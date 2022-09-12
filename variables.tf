variable "bucket_names" {
  type    = list(string)
  default = ["project-business-data", "project-twitter-data"]
}

variable "region" {
  default = "eu-west-1"
}

# variable "aws_access_key" {
# }

# variable "aws_secret_key" {
# }

# variable "TWITTER_TOKEN" {
# }

# variable "POSTGRES_HOST" {
#   sensitive = true
# }

# variable "POSTGRES_PORT" {
#   sensitive = true
# }

# variable "POSTGRES_DB" {
#   sensitive = true
# }

# variable "db_username" {
# }

# variable "db_password" {
#   type      = string
#   sensitive = true
# }