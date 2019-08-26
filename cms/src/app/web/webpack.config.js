const path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: {
    index: ['whatwg-fetch', './js/index.js'],
    main: './scss/main.scss'
  },
  mode: 'development',
  watch: false,
  watchOptions: {
    ignored: ['node_modules', 'dist']
  },
  output: {
    path: path.resolve(__dirname, '../static/app'),
    publicPath: '/static/'
  },
  module: {
    rules: [
      {
        test: /.scss$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].css',
              outputPath: 'css'
            }
          },
          {
            loader: 'extract-loader'
          },
          {
            loader: 'css-loader'
          },
          {
            loader: 'postcss-loader'
          },
          {
            loader: 'sass-loader'
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
              outputPath: 'images'
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
