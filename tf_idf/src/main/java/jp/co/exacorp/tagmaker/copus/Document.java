package jp.co.exacorp.tagmaker.copus;

import java.io.Serializable;
import java.util.Collection;
import java.util.TreeSet;

/**
 * <p>文書をあらわすJava Beanクラス。</p>
 * <p>要素として文書のファイルパス、記述されている全単語をあらわすWordのコレクションを
 * 保有している。同じファイルパスであるインスタンスは同一としてあつかうように
 * <code>java.lang.Comparable</code>実装されている。シリアライズ可能オブジェクト。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class Document implements Comparable<Document>, Serializable {

	/**
	 * <p>シリアルバージョンUID</p>
	 */
	private static final long serialVersionUID = 2L;

	/**
	 * <p>文書のファイルパス。</p>
	 */
	private String filePath = null;

	/**
	 * <p>文書内に格納されている全単語。</p>
	 */
	private Collection<Word> words = new TreeSet<Word>();

	/**
	 * <p>デフォルトコンストラクタ。</p>
	 */
	public Document(){}

	/**
	 * <p>文書のファイルパスを指定可能なコンストラクタ。</p>
	 * @param filePath 文書のファイルパス
	 */
	public Document(String filePath){ this.filePath = filePath; }

	/**
	 * <p>文書のファイルパスおよび文書に格納されている全単語コレクションを
	 * 指定可能なコンストラクタ。</p>
	 * @param filePath 文書のファイルパス
	 * @param words 全単語リスト
	 */
	public Document(String filePath, Collection<Word> words){ this(filePath); this.words = words; }

	/**
	 * <p>文書のファイルパスを取得する。</p>
	 * @return java.lang.String ファイルパス
	 */
	public String getFilePath(){ return this.filePath; }

	/**
	 * <p>文書のファイルパスを格納する。</p>
	 * @param filePath 新たなファイルパス
	 */
	public void setFilePath(String filePath){ this.filePath = filePath; }

	/**
	 * <p>文書内の全単語を取得する。</p>
	 * @return java.util.Collection&lt;jp.co.exacorp.keys.copus.Word&gt; 全単語リスト
	 */
	public Collection<Word> getWords(){ return this.words; }

	/**
	 * <p>文書内の全単語を格納する。</p>
	 * @param words 新しい全単語コレクション
	 */
	public void setWords(Collection<Word> words){ this.words = words; }

	/**
	 * <p>文書内に該当する単語があれば返却する。</p>
	 * @param text 単語を表す文字列
	 * @return jp.co.exacorp.keys.copus.Word 単語、無い場合はnullを返却する。
	 */
	public Word getWord(String text){
		for(Word word: words){
			if(word.getText().equals(text)) return word;
		}
		return null;
	}

	/**
	 * <p>単語を１件追加する。</p>
	 * @param word 追加対象の単語
	 */
	public void setWord(Word word){ this.words.add(word); }

	/**
	 * <p>指定した単語の文書内登場頻度を取得する。</p>
	 * @param text 単語を表す文字列
	 * @return int 登場頻度、登場しない場合は0を返却する。
	 */
	public int getFrequency(String text){
		Word word = getWord(text);
		if(word==null) return 0;
		return word.getFrequency();
	}

	/**
	 * <p>同じファイルパスの場合同一Documentとしてあつかう実装でオーバライド。</p>
	 * @param o 比較対象インスタンス
	 * @return boolean 比較結果を表す真偽値
	 */
	@Override
	public boolean equals(Object o){
		if(o instanceof Document){
			if(filePath==null) return false;
			return filePath.equals(((Document)o).getFilePath());
		}else{
			return false;
		}
	}

	/**
	 * <p>比較メソッド。</p>
	 * <p>要素filePathの実装を呼び出している。
	 * 同じファイルパスのDocumentインスタンスを同一扱いするようオーバライドされている。</p>
	 * @param o 比較対象インスタンス
	 * @return int 比較結果
	 */
	@Override
	public int compareTo(Document o) {
		if(this.filePath==null) return -1;
		return this.filePath.compareTo(o.getFilePath());
	}

	/**
	 * <p>Documentインスタンスの各要素の内容を表す文字列を返却する実装に
	 * オーバライドされている。</p>
	 * @return java.lang.String インスタンスの各要素の内容を表す文字列
	 */
	@Override
	public String toString(){
		StringBuilder msg = new StringBuilder();
		msg.append("[");
		msg.append(this.filePath);
		msg.append("{");
		for(Word word: this.words){
			msg.append(word.toString());
		}
		msg.append("}]");
		return msg.toString();
	}

	/**
	 * <p>ハッシュコード値を取得する。</p>
	 * <p><code>equals</code>メソッドオーバーライドしたため、
	 * 要素filePathのハッシュコード値を返却する実装となっている。</p>
	 * @return int 要素filePathのハッシュコード値
	 */
	@Override
	public int hashCode(){
		return this.filePath.hashCode();
	}
}

