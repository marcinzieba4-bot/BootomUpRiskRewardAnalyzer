#!/bin/bash
# Deploy VeeRock website to both S3 static (CloudFront) and EC2 (via tarball)
# Run this script with AWS credentials configured.

set -e

BUCKET="s3bucketmz"
STATIC_PREFIX="veerock-site/static"
REGION="eu-north-1"
CF_DIST_S3="E15IJW4438D21G"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBSITE_DIR="$SCRIPT_DIR/website"

echo "=== Building website ==="
cd "$WEBSITE_DIR"
npm install
npm run build

echo ""
echo "=== Uploading static export to S3 (CloudFront site) ==="
aws s3 sync out/ "s3://$BUCKET/$STATIC_PREFIX/" \
  --delete \
  --region "$REGION" \
  --cache-control "public, max-age=31536000, immutable" \
  --exclude "*.html" \
  --exclude "*.txt"

aws s3 sync out/ "s3://$BUCKET/$STATIC_PREFIX/" \
  --delete \
  --region "$REGION" \
  --cache-control "public, max-age=0, must-revalidate" \
  --exclude "*" \
  --include "*.html" \
  --include "*.txt"

echo ""
echo "=== Packaging tarball for EC2 ==="
cd "$WEBSITE_DIR"
tar -czf /tmp/veerock.tar.gz \
  app \
  components \
  next.config.mjs \
  package.json \
  package-lock.json \
  postcss.config.js \
  tailwind.config.ts \
  tsconfig.json \
  next-env.d.ts

aws s3 cp /tmp/veerock.tar.gz "s3://$BUCKET/veerock-site/veerock.tar.gz" --region "$REGION"
echo "Tarball uploaded — EC2 cron job will pick it up and redeploy."

echo ""
echo "=== Invalidating CloudFront cache ==="
aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_S3" \
  --paths "/*" \
  --region us-east-1

echo ""
echo "=== Done ==="
echo "CloudFront ($CF_DIST_S3): https://d7g7nkeytae81.cloudfront.net"
echo "EC2: http://16.16.218.231:3000 (redeploys in ~5 min via cron)"
