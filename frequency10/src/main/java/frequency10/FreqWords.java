package frequency10;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.TreeSet;

public class FreqWords {

	public static final String FILE_PATH = "data" + File.separator + "radio.txt";
	public static final int SIZE = 10;

	public static void main(String[] args) throws IOException {
		Map<String, Integer> words = new HashMap<String, Integer>();
		BufferedReader br =
				new BufferedReader(
						new InputStreamReader(
								new FileInputStream(FILE_PATH), "UTF-8"));
		String line = null;
		while((line = br.readLine()) != null){
			StringTokenizer st = new StringTokenizer(line, " ");
			while(st.hasMoreTokens()){
				String text = st.nextToken();
				Integer count = words.get(text);
				if(count == null){
					words.put(text, new Integer(1));
				}else{
					words.put(text, new Integer(count.intValue() + 1));
				}
			}
		}
		br.close();

		TreeSet<Word> orderedWords = new TreeSet<Word>();
		Set<String> keys = words.keySet();
		for(String key: keys){
			orderedWords.add(new Word(key, words.get(key)));
		}
		int pos = 0;
		for(Word word: orderedWords){
			if(pos++ >= SIZE){
				break;
			}
			System.out.println(word);
		}
	}

}
