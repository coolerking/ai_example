package frequency10;

public class Word implements Comparable<Word> {
	private String text = null;
	private int count = 1;
	public Word(String text, int count){
		this.text = text;
		this.count = count;
	}
	public String getText(){
		return text;
	}
	public void setText(String text){
		this.text = text;
	}
	public int getCount(){
		return count;
	}
	public void setCount(int count){
		this.count = count;
	}
	@Override
	public int compareTo(Word o) {
		if(this.count == o.getCount()){
			return this.text.compareTo(o.getText());
		}else{
			return o.getCount() - this.count;
		}
	}
	@Override
	public boolean equals(Object o){
		if(o instanceof Word){
			return this.equals(((Word)o).getText());
		}else{
			return false;
		}
	}
	@Override
	public int hashCode(){
		return this.text.hashCode();
	}
	@Override
	public String toString(){
		return text + "\t" + count;
	}
}
