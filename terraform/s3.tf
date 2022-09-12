resource "aws_s3_bucket" "project_buckets" {
  count  = length("${var.bucket_names}")
  bucket = var.bucket_names[count.index]
}
resource "aws_s3_bucket_acl" "project_buckets_acl" {
  count  = length("${var.bucket_names}")
  bucket = var.bucket_names[count.index]
  acl    = "private"
}

