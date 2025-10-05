/** @type {import('next').NextConfig} */
const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const nextConfig = {
  transpilePackages: ['kepler.gl'],
  webpack: (config, { isServer }) => {
    // Kepler.gl aliases
    config.resolve.alias = {
      ...config.resolve.alias,
      'kepler.gl/components': 'kepler.gl/dist/components',
      'kepler.gl/actions': 'kepler.gl/dist/actions',
      'kepler.gl/reducers': 'kepler.gl/dist/reducers',
    };

    // Enable async WebAssembly
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
    };

    // Copy the parquet WASM file into Next build output
    config.plugins.push(
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(
              __dirname,
              'node_modules/@loaders.gl/parquet/dist/parquet_wasm_bg.wasm'
            ),
            to: path.resolve(__dirname, '.next/server/chunks/'),
          },
        ],
      })
    );

    // Prevent fs module issues on client
    if (!isServer) {
      config.resolve.fallback = { fs: false };
    }

    return config;
  },
};

module.exports = nextConfig;
