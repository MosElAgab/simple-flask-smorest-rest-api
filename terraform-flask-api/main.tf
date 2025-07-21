resource "aws_key_pair" "flask_key" {
  key_name   = "flask-api-key"
  public_key = file("~/.ssh/flask-api-key.pub") # Make sure you have a public key
}

resource "aws_security_group" "flask_sg" {
  name        = "flask-api-sg"
  description = "Allows ssh and custom ports for app"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5007
    to_port     = 5007
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "flask_server" {
  ami                    = "ami-0150ccaf51ab55a51"
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.flask_key.key_name
  vpc_security_group_ids = [aws_security_group.flask_sg.id]
  tags = {
    Name = "flask-api-server"
  }
user_data = <<-EOF
  #!/bin/bash

  sudo dnf update -y
  sudo dnf install -y docker git make

  sudo systemctl enable docker
  sudo systemctl start docker

  sudo usermod -aG docker ec2-user
  
  curl -SL https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose

  git clone https://github.com/MosElAgab/simple-flask-smorest-rest-api.git /home/ec2-user/simple-flask-smorest-rest-api
  sudo chown -R ec2-user:ec2-user /home/ec2-user/simple-flask-smorest-rest-api
  
  EOF
}
output "instance_public_ip" {
  value = aws_instance.flask_server.public_ip
}
