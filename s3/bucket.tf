resource "aws_s3_bucket" "project_buckets" {
    count = length("${var.bucket_names}")
    bucket = "${var.bucket_names[count.index]}"
    acl = "${var.acl_value}"
    region = "${var.region}"
}