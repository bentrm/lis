const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
  entry: {
    index: ['whatwg-fetch', './js/index.js'],
    main: './scss/main.scss'
  },
  watch: false,
  watchOptions: {
    ignored: ['node_modules', 'dist']
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    publicPath: '/static/app/'
  },
  plugins: [
    // make sure to include the plugin!
    new VueLoaderPlugin()
  ],
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /.scss$/,
        use: [
          {
            loader: 'vue-style-loader',
          },
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
