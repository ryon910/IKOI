module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}', // pagesディレクトリの更新されたパス
    './src/components/**/*.{js,ts,jsx,tsx}', // componentsディレクトリの更新されたパス
  
    // './src/app/**/*.{js,ts,jsx,tsx,mdx}' // 既存のsrc/appディレクトリ なくてよいかも
  ],
  theme: {
    extend: {
      // ここにテーマをカスタマイズする設定を追加できます
    },
  },
  plugins: [
    require('daisyui'), // プラグインの追加方法を修正
  ],
  daisyui: {
    themes: [
      {
        mytheme: { // カスタムテーマの設定
          "primary": "#D1C1D7",
          "secondary": "#F6CBD1",
          "accent": "#B4E9D6",
          "neutral": "#70ACC7",
          "base-100": "#F9FAFB",
        },
      },
      "light",
      "pastel",
    ],
  },
}
