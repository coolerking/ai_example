// index.html上のbody一番最初のdivタグのid値
var MAIN_ELEMENT = "#main"
// index.html上のcanvasタグのid値
var CANVAS_ID = "canvas"

// Predictionクラス
var Prediction = (function () {
    // Predictionのコンストラクタを定義
    // image: 予測対象のイメージ
    // sample[0]: サンプルイメージ
    // sample[1]: サンプルデータ
    function Prediction(image, sample) {
        this.image = image;
        this.sampleImage = sample[0];
        this.sampleData = sample[1];
        this.result = -1;
    }

    // Prediction.prototype はPrototypeの親への参照

    // Predictionにenvelope(data)を定義
    // 引数data：Requestパラメータ
    // XSRF対応したJSON型式のdataを返却
    Prediction.prototype.envelop = function (data) {
        // " 引数= "に合致するCookieの値(ない場合はundefined)
        var getCookie = function(name){
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
        }
        // dataをJSON型式に
        var envelope = {
            // cookie内から "_xsrf"値を取得しJSONへセット
            _xsrf: getCookie("_xsrf"),
            // データ本体（配列）
            "data[]": data
        }
        // XSRF対応したJSON型式のdataを返却
        return envelope;
    }

    // PredictionにimageSrc()を定義
    // imageのURLを返却
    Prediction.prototype.imageSrc = function () {
        // imageのURLを返却
        return this.image.toDataURL();
    }

    // Predictionにexecute()を定義
    // Promise オブジェクトを返却
    Prediction.prototype.execute = function () {
        var self = this;
        // Defferedオブジェクトを生成
        var d = new $.Deferred;
        // POST送信
        // URL: "/predict"
        // POST時送信パラメータ： サンプルデータのXSRF対応したJSONデータ
        // 関数：コールバック関数
        $.post("/predict", self.envelop(self.sampleData), function(prediction){
            // "result"値を変数へ
            self.result = prediction["result"];
            // done()へselfを引数にわたし、状態を正常終了"resolved"に
            d.resolve(self)
        })
        // Promizeオブジェクトを返却
        return d.promise();
    };

    // Predictにfeedback(value)を定義
    Prediction.prototype.feedback = function (value) {
        var self = this;
        // Deferredオブジェクトを生成
        var d = new $.Deferred;
        // 引数を整数化して配列に
        var feedback = [parseInt(value)];
        // 配列feedbackにサンプルデータを連結
        feedback = feedback.concat(self.sampleData);
        // POST送信
        // URL: "/feedback"
        // POST時送信パラメータ： 引数value + サンプルデータ
        // 関数：コールバック関数
        $.post("/feedback", self.envelop(feedback), function(feedbacked){
            // "result"値が""の場合
            if(feedbacked["result"] == ""){
                // 引数value値で代替
                self.result = feedback[0];
                // 状態を正常終了"resolved"に
                d.resolve();
            // "result"値が""以外の場合
            }else{
                // fail("result"値)を実行し、状態を異常終了に
                d.reject(feedbacked["result"]);
            }
        })
        // Promizeオブジェクトを返却
        return d.promise();
    };

    // Predictionオブジェクトを返却
    return Prediction;
})();

// プレーンテキスト展開デリミタ{{,}}から[[,]]に変更
Vue.config.delimiters = ["[[", "]]"];
// ディレクティブのv-textのvにあたる部分をdata-v-に変更
Vue.config.prefix =  "data-v-";
// カスタム要素 <predict-item>の登録
Vue.component("predict-item", {
    //
    template: "#predict-item",
    methods: {
        // 編集開始
        beginEdit: function(){
            // 編集可能にセット
            this.state.editing = true;
        },
        // 編集終了
        endEdit: function(){
            // 状態を取得
            var state = this.state;
            // state.value 値が0～9 の範囲内でかつresult値と異なる場合
            if(state.value >= 0 && state.value < 10 && (state.value != this.result)){
                // 
                var original = this.result;
                this.$data.feedback(state.value).fail(function(msg){
                    state.value = original;
                })
            }else{
                state.value = this.result;
            }
            state.editing = false;
        }
    }
});
// rootインスタンスを生成し、変数appへ
var app = new Vue({
    // // index.html上のbody一番最初のdivタグ内に生成する
    el: MAIN_ELEMENT,
    data: {
        canvas: null,
        SNAP_SIZE: 120,
        SAMPLE_SIZE: 80,
        predicts: []
    },
    created: function(){
        this.canvas = new Canvas(CANVAS_ID, {
            strokeStyle: "black"
        });
    },
    methods:{
        clear: function(){
            this.canvas.clear();
        },
        injectState: function(p){
            p.state =  {
                editing: false,
                value: p.result
            }
        },
        submit: function(){
            var self = this;
            var image = self.canvas.snapShot(self.SNAP_SIZE);
            var sample = self.canvas.toSample(self.SAMPLE_SIZE, self.SAMPLE_SIZE);
            var total = sample[1].reduce(function(a, b){ return a + b; });
            if(total == 0){
                return false;
            }
            var p = new Prediction(image, sample);
            p.execute().done(function(p){
                self.injectState(p);
                self.predicts.unshift(p);
                self.clear();
            })
        }
    }
});
