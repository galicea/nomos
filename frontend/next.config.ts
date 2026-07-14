const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({
  output: 'export',
  images: { unoptimized: true },
  reactCompiler: true,
  reactStrictMode: true,
  trailingSlash: true,
  cleanDistDir: true,
  // Twoje pozostałe konfiguracje Next.js
})
