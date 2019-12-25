package jp.co.exacorp.tagmaker;

import java.util.Collection;
import java.util.Iterator;

import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;
/**
 * <p>TF-IDF計算ユーティリティクラス。</p>
 * <p>TF-IDF計算を実装する本体となるクラス。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class TFIDFUtils {

	/**
	 * <p>TF-IDF値を求める。TF(t,d)とIDF(d)を積算した行列となる。</p>
	 * @param documents 全文書リスト
	 * @param words タグ候補単語リスト
	 * @return double[][] TFIDF(t,d) TFIDF値(t:単語(1次元目)、d:文書(2次元目))
	 */
	public static double[][] computeTFIDF(
			Collection<Document> documents, Collection<Word> words){
		double[][] tf = computeTF(documents, words);
		double[] idf = computeIDF(documents, words);
		double[][] tfidf = new double[words.size()][documents.size()];
		for(int t=0; t<words.size();t++){
			for(int d=0; d<documents.size(); d++){
				tfidf[t][d] = tf[t][d] * idf[t];
			}
		}
		return tfidf;
	}

	/**
	 * <p>TF(Term Frequency)値を求める。TF(t,d)を計算する場合、</p>
	 * <ul>
	 * <li>分子：ある単語 t の文書 d 内での出現回数</li>
	 * <li>分母：文書d内のすべての単語の出現回数の和</li>
	 * </ul>
	 * <p>を計算した値となる指標で、登場頻度が増えれば値が大きくなる。</p>
	 * @param documents 全文書リスト
	 * @param words タグ候補単語リスト
	 * @return double[][] TF(t, d) 値(t：単語(1次元目)、d：文章(2次元目))
	 */
	public static double[][] computeTF(
			Collection<Document> documents, Collection<Word> words){
		// 分母の計算
		double[] total = new double[documents.size()];
		Iterator<Document> it = documents.iterator();
		for(int d=0;d<total.length;d++){
			total[d] = 0D;
			Collection<Word> _words = it.next().getWords();
			for(Word _word: _words){
				total[d] += ((double)_word.getFrequency());
			}
		}

		// 結果配列：初期化
		double[][] tf = new double[words.size()][documents.size()];
		for(int t=0; t<tf.length; t++) for(int d=0; d<tf[t].length; d++) tf[t][d] = 0D;

		// TF値の計算
		int t=0;
		for(Word word: words){
			int d=0;
			for(Document document: documents){
				tf[t][d] = ((double) document.getFrequency(word.getText())) / total[d];
				d++;
			}
			t++;
		}

		// 結果配列の返却
		return tf;
	}

	/**
	 * <p>IDF(Inverse Document Frequency)値を求める。IDF(t)を計算する場合、</p>
	 * <ul>
	 * <li>分子：全文書数＋１</li>
	 * <li>分母：単語tが出現する文書数＋１</li>
	 * </ul>
	 * <p>の対数＋１となる値を計算した指標で、文書横断的に使用されている単語の値が低くなる。
	 * なお、本実装では補正値１を各々加えており、一般的なIDF値とは異なっていることに注意。</p>
	 * @param documents 全文書リスト
	 * @param words タグ候補単語リスト
	 * @return double[] IDF(t)値 (t：単語(1次元目))
	 */
	public static double[] computeIDF(
			Collection<Document> documents, Collection<Word> words){
		// 結果配列
		double[] idf = new double[words.size()];
		// 分子（文書数）
		double n = ((double) documents.size());

		Iterator<Word> it = words.iterator();
		for(int t=0; t<idf.length; t++){
			String text = it.next().getText();
			int count = 0;
			for(Document document: documents){
				if(document.getFrequency(text)>0) count++;
			}
			idf[t] = Math.log(( (n + 1.0D) / ( ((double) count) + 1.0D ))) + 1.0D;
		}

		// 結果配列の返却
		return idf;
	}
}
