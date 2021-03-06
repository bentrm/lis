const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const env = process.env.NODE_ENV;
const isProd = env === 'production';
const distDir = path.resolve(__dirname, 'dist');
const cmsHost = process.env.CMS_URL;
let langHosts = process.env.LANG_HOSTS;

if (langHosts) {
  const arr = {};
  langHosts.split(';').map(x => x.split('=')).forEach(([host, lang]) => {
    arr[host] = lang;
  });
  langHosts = arr;
}

const plugins = [
  new CleanWebpackPlugin(),
  new HtmlWebpackPlugin({
    title: 'LIS',
    template: './src/index.html'
  }),
  new VueLoaderPlugin(),
  new webpack.DefinePlugin({
    __CMS__: JSON.stringify(cmsHost),
    __LANG_HOSTS__: JSON.stringify(langHosts || {})
  }),
];

if (isProd) {
  plugins.push(
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',
    })
  );
}


module.exports = {
  mode: env || 'development',
  entry: {
    index: ['whatwg-fetch', './src/js/index.js'],
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      'vue-meta$': 'vue-meta/dist/vue-meta.esm.js',
      'vue-router$': 'vue-router/dist/vue-router.esm.js',
      'vuex$': 'vuex/dist/vuex.esm.js',
      'vue2-leaflet$': 'vue2-leaflet/dist/vue2-leaflet.es'
    }
  },
  devtool: isProd ? 'source-map' : 'eval-source-map',
  devServer: {
    historyApiFallback: true,
    contentBase: distDir,
    host: '0.0.0.0',
    port: 3000
  },
  watch: false,
  watchOptions: {
    ignored: ['node_modules', 'dist']
  },
  output: {
    path: distDir,
    filename: '[name].bundle.[contenthash].js',
    publicPath: '/'
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      name: 'vendor'
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
                useBuiltIns: 'usage',
                corejs: {
                  version: 3,
                  proposols: true
                },
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
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
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
              outputPath: 'files/'
            }
          }
        ]
      }
    ]
  }
};
