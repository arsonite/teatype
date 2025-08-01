module.exports = class KGenerator extends Module {
  getContent() {
    return p();
  }
};

/*
public class RandomSum {
	public static void main(String[] args) {
		PrintWriter out = new PrintWriter(System.out, true);
		Random r = new Random();

		int min = 12500;
		int max = 13000 - min;
		int sum = (int) (Math.random()*max+min);

		double[] a = randomGenerate(31, 350, 450, sum, r);
		double[] l = new double[20];
		double k = 0;
		
		for(int i = 0; i < l.length; i++) {
			l[i] = ((double) i/100) * 5;
		}

		for (int i = 0; i < a.length; i++) {
			a[i] = a[i] + l[r.nextInt(l.length)];
			k+= a[i];
			out.printf("Tag %d: %.2f €%n", i+1, a[i]);
		}
		out.printf("%nSumme: %.2f €", k);
	}

	public static double[] randomGenerate(int days, int min, int max, int tempMax, Random r) {
		double[] nums = new double[days];
		int maxSum = tempMax - min*days;

		for(int i = 1; i < nums.length; i++) {
			nums[i] = r.nextInt(maxSum);
		}

		Arrays.sort(nums, 0, nums.length);

		for(int i = 1; i < nums.length; i++) {
			nums[i-1] = nums[i] - nums[i-1] + min;
		}

		nums[nums.length-1] = maxSum - nums[nums.length-1] + min;
		return nums;
	}
}
*/

/*
public class RandomNumberGen {
	public RandomNumberGen() {
	}

	public int[][] generateNumbers() {
		while(c < 1) {
			v++;
			for(int i = 0; i < d; i++) {
				x = (int) (Math.random()*q+n);
				i2[i] = x;
				k+= i2[i];
			}

			for(int i = 0; i < d; i++) {
				if(k>s1 && k<s2) {
					wochentage.append(i2[i] + "," + y[rnd.nextInt(y.length)] + "\n");
					if(k>s1 && k<s2) {
						c++;
						ergebnis1.setText("≈ " + k + "€");
					} else { 
						continue;
					}
				}
			}
		}

		long stopTime = System.currentTimeMillis();
		long time = stopTime - startTime;

		tries.setText("Rechenversuche: " + v + " Zeit in ms: " + time);

		//Wochenend-Generations-Schleife
		for(int i = 0; i < w; i++) {
			x2 = (int) (Math.random()*100+300);
			i3[i] = x2;
		}

		for(int i = 0; i < w; i++) {
			k2+= i3[i];
		}

		for(int i = 0; i < w; i++) {
			wochenende.append("\n" + i3[i] + "," + y[rnd.nextInt(y.length)]);
			count++;
			if((count)%2==0) {
				wochenende.append("\n");
			}
		}
		ergebnis2.setText("≈ " + k2 + "€");
	}

	public String err() {
		return "No valid input.";
	}
}
*/
