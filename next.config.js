/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  transpilePackages: ['kepler.gl'],
  webpack: (config, { isServer }) => {
    // Fix alias for Kepler.gl
    config.resolve.alias = {
      ...config.resolve.alias,
      'kepler.gl/components': 'kepler.gl/dist/components',
      'kepler.gl/actions': 'kepler.gl/dist/actions',
      'kepler.gl/reducers': 'kepler.gl/dist/reducers',
    };

    // Allow WebAssembly files to be properly handled
    config.experiments = { ...config.experiments, asyncWebAssembly: true };

    // Copy parquet_wasm_bg.wasm to the .next directory during build
    config.module.rules.push({
      test: /parquet_wasm_bg\.wasm$/,
      type: 'asset/resource',
      generator: {
        filename: 'static/chunks/[name][ext]',
      },
    });

    // Fix: ensure wasm files are loaded correctly at runtime
    if (!isServer) {
      config.resolve.fallback = { fs: false };
    }

    return config;
  },
};

module.exports = nextConfig;
