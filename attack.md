Graphs bro
 make em
1mb -> 11mb cbr
 dr, tp, lat

1mb -> 11mb cbr
time deltas
 dr, tp, lat

probabilities bro
 do em

variance and shit

-----------------------

Repeat exp1 with varied start
intervals

create graphs of averages

which TCP variants are able to get higher average throughput?
Which has the lowest average latency?
Which has the fewest drops?
Is there an overall "best" TCP variant in this experiment, or does the "best" variant vary depending on other circumstances? 

----------------------
exp2

fairness

construct graphs comparing
latency
droprate
throughput
of pairwise combinations

are the different combinations of variants fair to each other?
Are there combinations that are unfair, and if so, why is the combination unfair?
To explain unfairness, you will need to think critically about how the protocols are implemented and why the different choices in different TCP variants can impact fairness. 

----------------------

Intro: 5% of your grade. Your intro should explain what it is that you are studying and motivate why this is an important problem to study. Good introductions also include a "preview" that highlights the major experiments you will be presenting, and some of your key results.

The importance of understanding Congestion and Fairness

Methodology: 10% of your grade. The methodology section should clearly explain how your experiments were conducted. What tools were used? Why did you choose to use these tools, and how do you know they are sound? What were the key parameters/variables/settings used during the experiments? Why did you choose these values?

ns-2, python, pyplot, shell scripts, CBR, tcp agents, varying start times

Results for Experiment 1: 30% of your grade. Present and thoroughly analyze the results from the first set of experiments. Explain why the results are the way they are by discussing how the different TCP variants react to the presence of congestion. Does each variant behave the same way, and if not, why not?

Congestion, 
 reno
 newreno
 vegas
 tahoe

Results for Experiment 2: 30% of your grade. Thoroughly and carefully present the results from the two-TCP stream experiments. When there are two TCP streams, do they share bandwidth fairly, and if not, why not? If there are any unexpected or "shocking" findings, highlight them in your text and discuss what leads to these results.

reno/reno
newreno/reno
vegas/vegas
newreno/vegas


Conclusion: 5% of your grade. Restate the significance of your study and highlight key results. Discuss the real-world significance of your results, and what the implications may be on deployed systems. Highlight any open questions that may motivate future studies.

key results:

real world significance:

deployed implications:

open questions:

