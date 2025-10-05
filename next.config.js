/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  transpilePackages: ['kepler.gl'],
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      'kepler.gl/components': 'kepler.gl/dist/components',
      'kepler.gl/actions': 'kepler.gl/dist/actions',
      'kepler.gl/reducers': 'kepler.gl/dist/reducers'
    }
    return config
  }
}

module.exports = nextConfig