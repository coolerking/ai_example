/**
 *
 */
package jp.co.exacorp.tagmaker;

import static org.junit.Assert.*;

import java.io.File;
import java.io.IOException;
import java.util.Collection;
import java.util.Iterator;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import jp.co.exacorp.tagmaker.copus.Document;
import jp.co.exacorp.tagmaker.copus.Word;

/**
 * <p>TMContextの疎通動作確認用テストクラス。</p>
 * <p>ワークスペース内の <code>data/test</code> 以下のデータを使用する。</p>
 *
 * @author Tasuku Hori
 * (C) Tasuku Hori, exa Corporation Japan, 2017. All rights reserved.
 */
public class TMContextTest {

	/**
	 * <p>テストデータのベースディレクトリ。</p>
	 */
	public static final String BASEDIR = "data" + File.separator + "test";

	/**
	 * <p>ソースディレクトリ。</p>
	 */
	public static final String SRCDIR = BASEDIR + File.separator + "src";

	/**
	 * <p>一時ファイル格納用ディレクトリ。</p>
	 */
	public static final String TMPDIR = BASEDIR + File.separator + "tmp";

	/**
	 * <p>結果格納用ディレクトリ。</p>
	 */
	public static final String RESULTDIR = BASEDIR + File.separator + "result";

	/**
	 * <p>コンテキストインスタンス。本クラスのテスト対象となる。</p>
	 */
	private TMContext context = null;

	/**
	 * <p>テスト開始時処理。</p>
	 * <p>本クラスのテスト対象であるコンテキストインスタンスを生成する。</p>
	 */
	@Before
	public void setUp(){
		try{
			this.context = new TMContext(SRCDIR, TMPDIR, RESULTDIR);
		}catch(RuntimeException re){
			fail("Eval miss!");
		}
		File[] files = new File(TMPDIR).listFiles();
		if(files!=null && files.length>0){
			for(File file: files){
				file.delete();
			}
		}
		files = new File(RESULTDIR).listFiles();
		if(files!=null && files.length>0){
			for(File file: files){
				file.delete();
			}
		}
	}

	/**
	 * <p><code>getDocuments()</code> テストメソッド。</p>
	 */
	@Test
	public void test_getDocuments(){
		Collection<Document> documents = null;
		try {
			documents = context.getDocuments();
		} catch (ClassNotFoundException | IOException e) {
			fail("[test_getDocuments] serialize operation exception");
		}
		assertEquals(documents.size(), 3);
		Iterator<Document> it = documents.iterator();
		Document document = it.next();
		assertEquals(document.getWords().size(), 3);
		document = it.next();
		assertEquals(document.getWords().size(), 2);
		document = it.next();
		assertEquals(document.getWords().size(), 1);
		assertFalse(it.hasNext());
	}

	/**
	 * <p><code>getWords()</code>テストメソッド</p>
	 */
	@Test
	public void test_getWords() {
		Collection<Document> documents = null;
		try {
			documents = context.getDocuments();
		} catch (ClassNotFoundException e) {
			fail("[test_getWords] serialize operation exception");
		} catch (IOException e) {
			fail("[test_getWords] file operation exception");
		}
		Collection<Word> words = null;
		try {
			words = context.getWords(documents);
		} catch (IOException e) {
			fail("[test_getWords] file operation exception");
		}
		assertEquals(documents.size(), 3);
		Iterator<Word> it = words.iterator();
		Word word = it.next();
		assertEquals(word.getText(), "C");
		word = it.next();
		assertEquals(word.getText(), "B");
		word = it.next();
		assertEquals(word.getText(), "A");
		assertFalse(it.hasNext());

	}

	/**
	 * <p><code>compute()</code> テストメソッド</p>
	 */
	@Test
	public void testcompute() {
		double[][] expected = {
				{0.3333333333333333,	0.5,					1.0},
				{0.42922735748392693,	0.6438410362258904,		0.0},
				{0.5643823935199818,	0.0,					0.0}};
		try{
			Collection<Document> documents = context.getDocuments();
			Collection<Word> words = context.getWords(documents);
			double[][] result = context.compute(documents, words);
			for(int t=0;t<words.size();t++){
				for(int d=0; d<documents.size();d++){
					assertEquals(result[t][d], expected[t][d], 0.0000001);
				}
			}
		}catch(Exception e){
			fail("[compute] ]exception occurs!");
		}
	}

	/**
	 * <p><code>toString()</code> テストメソッド</p>
	 */
	@Test
	public void test_toString(){
		// デバッグ用なので出力があればOK
		assertNotNull(context.toString());
	}

	/**
	 * <p>テスト終了時処理。</p>
	 * <p>コンテキストインスタンスを開放する。</p>
	 */
	@After
	public void tearDown() {
		this.context = null;
	}
}
