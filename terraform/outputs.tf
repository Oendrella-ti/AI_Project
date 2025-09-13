output "chatbot_url" {
  value = "http://${aws_instance.chatbot_instance.public_ip}:5000"
}
