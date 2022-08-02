data "archive_file" "twitter_extract" {
    type = "zip"
    source_file = "generate_data/twitter_extract.py"
    output_path = "lambda_files/twitter_extract.zip"
}