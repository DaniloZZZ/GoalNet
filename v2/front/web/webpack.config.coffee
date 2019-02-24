path = require 'path'
webpack = require 'webpack'
{ rules, loaders, plugins, stats } = require('webpack-atoms')

browsers = ['last 2 versions', 'ie >= 10', 'not android <= 4.4.3']
HtmlWebpackPlugin = require 'html-webpack-plugin'
ExtractTextPlugin = require 'extract-text-webpack-plugin'

isProduction = process.env.NODE_ENV is 'production'

cssDev = ['style-loader', 'css-loader']
cssProd = ExtractTextPlugin.extract
  fallback: 'style-loader'
  use: ['css-loader']
  publicPath: '/dist'

cssConfig = if isProduction then cssProd else cssDev

HtmlWebpackPluginConfig = new HtmlWebpackPlugin
  template: './src/index.html'
  filename: 'index.html'
  hash: true

module.exports =
  entry: './src/index.coffee'
  output:
    filename: 'index.bundle.js'
    path: path.resolve(__dirname, 'dist')
    publicPath: '/'
  devServer:
    contentBase: path.join(__dirname, 'dist'),
    compress: true
    hot: true
    open: true
    historyApiFallback: true,
    headers:
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "content-type, Authorization, x-id, Content-Length, X-Requested-With",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS"
  module:
    rules: [
      {
        test: /\.coffee$/,
        use: [
          {
            loader: 'babel-loader'
            options:
              presets: ['env', 'react']
          }
          'coffee-loader'
        ],
        exclude: /node_modules/
      },
      {
        test: /\.less$/,
        use: [{
          loader: 'style-loader' ,
        }, {
          loader: 'css-loader',
        }, {
          loader: 'less-loader',
        }],
      },
      rules.js({}),
      #rules.less({ browsers }),
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      #{ oneOf: [rules.css.modules(), rules.css()] },
      #{ test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel-loader'] },

    ]
  plugins: [
    HtmlWebpackPluginConfig
    new ExtractTextPlugin
      filename: 'app.css'
      disable: !isProduction
      allChunks: true
    new webpack.HotModuleReplacementPlugin()
    new webpack.NamedModulesPlugin()
  ]
