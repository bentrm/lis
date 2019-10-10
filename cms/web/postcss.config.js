const env = process.env.NODE_ENV;
const isProd = env === 'production';
const plugins = [
  require('autoprefixer')
];

if (isProd) {
  plugins.push(
    require('postcss-preset-env'),
    require('cssnano')
  );
}

module.exports = {
  plugins,
};
