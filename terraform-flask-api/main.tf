resource "aws_key_pair" "flask_key" {
  key_name   = "flask-api-key"
  public_key = file("~/.ssh/flask-api-key.pub")  # Make sure you have a public key
}
