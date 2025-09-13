provider "aws" {
  region = var.aws_region
}

resource "aws_key_pair" "chatbot_key" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "chatbot_sg" {
  name = "chatbot-sg"

  ingress = [
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      from_port   = 5000
      to_port     = 5000
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]

  egress = [{
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }]
}

resource "aws_instance" "chatbot_instance" {
  ami                    = "ami-00ca32bbc84273381" # Amazon Linux 2
  instance_type          = var.t2.micro
  key_name               = var.key_name
  security_groups        = [aws_security_group.chatbot_sg.name]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install python3 git -y
    pip3 install flask gunicorn openai pinecone-client
    cd /home/ec2-user
    git clone ${var.github_repo}
    cd $(basename ${var.github_repo} .git)
    nohup gunicorn -w 4 app:app -b 0.0.0.0:5000 &
  EOF

  tags = {
    Name = "AI-Chatbot"
  }
}
