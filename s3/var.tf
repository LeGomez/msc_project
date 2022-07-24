variable "bucket_names" {
    type = list
    default = ["luis-project-twitter-data", "luis-project-business-data"]
}

variable "acl" {
    default = "private"
}

variable "region" {
    default = "eu-west-1"
}