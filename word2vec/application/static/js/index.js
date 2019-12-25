// filename: index.js
// require vue.js 2 library
//  see https://jp.vuejs.org/index.html
// (C) Tasuku Hori, exa Corporation Japan, 2017 all rights reserved.

// キーに合致するCookie値を取得する
function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : '2|4cdb01ba|98d5046a0c427a2fff3dedc176606622|1506334362';
}

Vue.component('word2vec-word', {
    props: ['word2vec'],
    template: '<li>{{ word2vec.text }} (確度: {{ word2vec.probability }})</li>'
})


// Vueインスタンスを生成
new Vue({
    // id値がappである要素を取得
    el: '#app',
    data: {
        // 入力エリアの値にv-modelで連携
        word2vec_input: '',
        // 出力エリア：初期値はなにもなし
        word2vec_output: []
    },
    methods: {
        // ボタン要素のv-on:click属性で指定されたJavaScript関数
        update: function(wakati_input){
            var that = this; // コールバック関数にバインドしていないので
            let params = new URLSearchParams();
            // 入力値をパラメータ化
            params.append('input_text', this.word2vec_input);
            // クロスサイトスクリプティング対策
            params.append('_xsrf', getCookie('_xsrf'));
            // vue推奨のaxiosを使ってAJAX
            axios.post("/predict", params)
            // 正常時コールバック関数
            .then(response => {
                // console.log(response.data);
                // 分かち書き済みデータを出力エリアへ書き出し
                this.word2vec_output = response.data.output_text;
            }) // then()
            .catch(error => {
                console.log(error);
            }); // catch()
        } // update()
    } // methods
}) // Vue({})

/** eof */
