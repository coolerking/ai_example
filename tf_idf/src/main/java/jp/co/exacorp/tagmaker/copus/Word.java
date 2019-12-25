package jp.co.exacorp.tagmaker.copus;

import java.io.Serializable;


/**
 * <p>単語を表す Java Bean クラス。</p>
 * <p>要素として単語を表す文字列と、文書内に登場する頻度を格納できる。
 * 単語を表す文字列が同一であれば同じインスタンスとして認識するように
 * Comparableを実装している。シリアライズ可能オブジェクト。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class Word implements Serializable, Comparable<Word> {

	/**
	 * <p>シリアルバージョンUID</p>
	 */
	private static final long serialVersionUID = 1L;

	/**
	 * <p>単語を表す文字列</p>
	 */
	private String text = "";

	/**
	 * <p>登場頻度</p>
	 */
	private int frequency = 1;

	/**
	 * <p>デフォルトコンストラクタ。</p>
	 * <p>単語を表す文字列は空文字、登場頻度は1としてインスタンス化される。</p>
	 */
	public Word(){}

	/**
	 * <p>登場頻度は1としてインスタンス化されるコンストラクタ。</p>
	 * @param text 単語を表す文字列
	 */
	public Word(String text){ this.text = text; }

	/**
	 * <p>全ての要素を引数として指定可能なコンストラクタ。</p>
	 * @param text 単語を表す文字列
	 * @param frequency 登場頻度を表す数値
	 */
	public Word(String text, int frequency){ this(text); this.frequency = frequency; }

	/**
	 * <p>単語を表す文字列を返却。</p>
	 * @return java.util.String 単語を表す文字列
	 */
	public String getText(){ return this.text; }

	/**
	 * <p>単語を表す文字列を格納する。</p>
	 * @param text 単語を表す文字列
	 */
	public void setText(String text){ this.text = text; }

	/**
	 * <p>登場頻度を取得する。</p>
	 * @return int 登場頻度
	 */
	public int getFrequency(){ return this.frequency; }

	/**
	 * <p>登場頻度を格納する。</p>
	 * @param frequency 登場頻度
	 */
	public void setFrequency(int frequency){ this.frequency = frequency; }

	/**
	 * <p>比較メソッドをオーバライドし、
	 * textが同じものは同一、その他は登場頻度の降順にならべる実装に変更。</p>
	 * @param o 比較対象のWordインスタンス
	 * @return int 比較結果
	 */
	@Override
	public int compareTo(Word o) {
		if(this.frequency == o.getFrequency()) return text.compareTo(o.getText());
		return o.getFrequency() - this.frequency;
	}

	/**
	 * <p>単語を表す文字列が同一の場合同じインスタンスであると認識する実装にオーバライド。</p>
	 * @param o 比較対象
	 * @return boolean 同一かどうかの真偽値
	 */
	@Override
	public boolean equals(Object o){
		if(o instanceof Word){
			return this.text.equals(((Word)o).getText());
		}else{
			return false;
		}
	}

	/**
	 * <p>デバッグ用として要素を表す文字列を返却する実装にオーバライド。</p>
	 * @return java.util.String 各要素を表す文字列
	 */
	@Override
	public String toString(){
		return "[" + this.text + "(" + this.frequency + ")]";
	}

	/**
	 * <p>ハッシュコード値を返却する。</p>
	 * <p><code>equals</code>メソッドオーバライドのため、要素textのハッシュコードを返却するように
	 * 実装を変更する。</p>
	 * @return int 要素textのハッシュコード値
	 */
	@Override
	public int hashCode(){
		return this.text.hashCode();
	}
}
