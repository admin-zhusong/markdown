#!/bin/bash

# 部署配置
SERVER="47.98.205.180"
USER="root"
PROJECT_DIR="/opt/markdown_work"
VENV_DIR="/opt/markdown_work/venv"

echo "=== 开始部署 Markdown 编辑器项目 ==="

# 1. 创建远程目录
echo "1. 创建远程目录..."
ssh $USER@$SERVER "mkdir -p $PROJECT_DIR"

# 2. 上传项目文件
echo "2. 上传项目文件..."
scp -r * $USER@$SERVER:$PROJECT_DIR/

# 3. 安装依赖
echo "3. 安装依赖..."
ssh $USER@$SERVER "
    # 安装 Python 和虚拟环境
    if ! command -v python3 &> /dev/null; then
        apt update && apt install -y python3 python3-pip python3-venv
    fi
    
    # 创建虚拟环境
    python3 -m venv $VENV_DIR
    
    # 激活虚拟环境并安装依赖
    source $VENV_DIR/bin/activate
    pip install -r $PROJECT_DIR/requirements.txt
    
    # 安装 gunicorn
    pip install gunicorn
"

# 4. 配置项目
echo "4. 配置项目..."
ssh $USER@$SERVER "
    cd $PROJECT_DIR
    
    # 创建数据库迁移
    source $VENV_DIR/bin/activate
    python manage.py makemigrations
    python manage.py migrate
    
    # 创建管理员账户
    echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123')\" | python manage.py shell
    
    # 收集静态文件
    python manage.py collectstatic --noinput
"

# 5. 配置 Nginx
echo "5. 配置 Nginx..."
ssh $USER@$SERVER "
    # 安装 Nginx
    if ! command -v nginx &> /dev/null; then
        apt install -y nginx
    fi
    
    # 创建 Nginx 配置
    cat > /etc/nginx/sites-available/markdown_work << 'EOF'
server {
    listen 80;
    server_name 47.98.205.180;

    location /static/ {
        alias $PROJECT_DIR/static/;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

    # 启用站点配置
    ln -sf /etc/nginx/sites-available/markdown_work /etc/nginx/sites-enabled/
    
    # 测试配置并重启
    nginx -t
    systemctl restart nginx
"

# 6. 启动 Gunicorn 服务
echo "6. 启动 Gunicorn 服务..."
ssh $USER@$SERVER "
    cd $PROJECT_DIR
    source $VENV_DIR/bin/activate
    
    # 创建 systemd 服务
    cat > /etc/systemd/system/markdown_work.service << 'EOF'
[Unit]
Description=Markdown Editor Gunicorn Service
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$VENV_DIR/bin/gunicorn --workers=3 --bind=127.0.0.1:8000 webmdeditor.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

    # 启动服务
    systemctl daemon-reload
    systemctl start markdown_work
    systemctl enable markdown_work
"

echo "=== 部署完成 ==="
echo "项目已部署到 http://47.98.205.180"
echo "管理员账户: admin / admin123"
