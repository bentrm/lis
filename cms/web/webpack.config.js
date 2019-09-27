const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const env = process.env.NODE_ENV;
const isProd = env === 'production';


const plugins = [
  new CleanWebpackPlugin(),
  new VueLoaderPlugin(),
];

if (isProd) {
  plugins.push(
    new MiniCssExtractPlugin({
      filename: 'css/[name].css',
      chunkFilename: 'css/[id].css'
    })
  );
}


module.exports = {
  mode: env || 'development',
  entry: {
    index: ['whatwg-fetch', './js/index.js'],
  },
  devtool: isProd ? 'source-map' : 'eval-source-map',
  watch: false,
  watchOptions: {
    ignored: ['node_modules', 'dist']
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/static/app/'
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      name: 'vendor',
    }
  },
  plugins,
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                useBuiltIns: 'entry',
                corejs: '3.2',
              }]
            ]
          }
        }
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          isProd ? MiniCssExtractPlugin.loader : 'vue-style-loader',
          'css-loader',
          'postcss-loader',
          'resolve-url-loader',
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
            }
          }
        ]
      },
      {
        test: /\.(png|jpe?g|gif)$/i,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'images/'
            }
          },
        ],
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/'
            }
          }
        ]
      }
    ]
  }
};
