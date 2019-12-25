package jp.co.exacorp.tagmaker;

import java.util.Collection;
import java.util.TreeSet;

import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;

/**
 * <p>コーパスユーティリティクラス。</p>
 * <p><code>jo.co.exacorp.tagmaker.copus</code>パッケージのJava Bean操作に関する
 * ユーティリティメソッド群を提供する。</p>
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All right reserved.
 */
public class CopusUtils {

	/**
	 * <p>全文書コレクションから、全単語コレクションを抽出する。</p>
	 * <p>作成されたコレクションは登場頻度の降順に整列された状態となっている。</p>
	 * @param documents 全文書コレクション
	 * @return java.util.Collection&lt;jp.co.exacorp.tagmaker.copus.Word&gt; 全単語コレクション
	 */
	public static Collection<Word> getVocabulary(Collection<Document> documents){
		Collection<Word> words = new TreeSet<Word>();
		if(documents == null || documents.size()==0) return words;
		for(Document document: documents){
			Collection<Word> _words = document.getWords();
			for(Word _word: _words){
				Word word = CopusUtils.search(words, _word.getText());
				if(word==null){
					word = new Word(_word.getText(), _word.getFrequency());
					words.add(word);
				}else{
					word.setFrequency(word.getFrequency() + _word.getFrequency());
				}
			}
		}
		Collection<Word> newWords = new TreeSet<Word>();
		for(Word word: words){
			newWords.add(word);
		}
		return newWords;
	}

	/**
	 * <p>引数で渡された全単語コレクションから該当する単語インスタンスを抽出する。</p>
	 * @param words 全単語コレクション
	 * @param text 単語のテキスト
	 * @return jp.co.exacorp.tagmaker.copus.Word 抽出した単語、存在しない場合nullを返却
	 */
	public static Word search(Collection<Word> words, String text){
		if(words==null || words.size()==0) return null;
		for(Word word: words){
			if(word!=null && word.getText().equals(text)){
				return word;
			}
		}
		return null;
	}
}