resource "aws_key_pair" "flask_key" {
  key_name   = "flask-api-key"
  public_key = file("~/.ssh/flask-api-key.pub")  # Make sure you have a public key
}

resource "aws_security_group" "flask_sg" {
    name = "flask-api-sg"
    description = "Allows ssh and custom ports for app"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    
    ingress {
        from_port = 5007
        to_port = 5007
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "flask_server" {
    ami = "ami-0150ccaf51ab55a51"
    instance_type = "t2.micro"
    key_name = aws_key_pair.flask_key.key_name
    vpc_security_group_ids = [aws_security_group.flask_sg.id]
    tags = {
        Name = "flask-api-server"
    }
}

output "instance_public_ip" {
  value = aws_instance.flask_server.public_ip
}
