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
  It depends on the CBR. At 8mb CBR out of a 10mb pipe vegas was able to maintain
  a surprisingly high average at .72 Mb/s. A full .1 Mb/s over new reno. 
  Tahoe, reno, and new reno behave simliarly with new reno beating the two previous incarnations in all brackets.
  closing in a win over the 
Which has the lowest average latency?
  The data says tahoe but I doubt this.

Which has the fewest drops?
  Vegas had the fewest drops.

Is there an overall "best" TCP variant in this experiment, or does the "best" variant vary depending on other circumstances? 
  Vegas would be the winner if it didnt have such high latency and behave poorly when the netowork is at 90% usage. If low latency is a necessity and the network has high utlization new reno may be better choice.

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

 No, especaially at certain network utilization levels. In my expiriments vegas was unfair to itself on a network of 7mb CBR. Similiar competitive behavior was obsvered with reno reno at high network utilzation though there was no persistent dominator in this situation.
 New reno beats out vegas across all CBR.

To explain unfairness, you will need to think critically about how the protocols are implemented and why the different choices in different TCP variants can impact fairness. 

----------------------

Intro: 5% of your grade. Your intro should explain what it is that you are studying and motivate why this is an important problem to study. Good introductions also include a "preview" that highlights the major experiments you will be presenting, and some of your key results.

Understanding congestion is important because protocols behave differently under varying levels of network activity. To build a reliable network these subtle behaviors within the various tcp agents must be understood and analysed.


Fairness is akin in this regard, as the interaction between various tcp agents can cause detrimental effects to network stability if their nature is misunderstood or unknown. Investigating the behavior of protocols in simulators allows for suppositions to be crafted with supporting evidence which can be tested on the open networks. Network simulators allow for hypothesis to be forumlated over the observed controlled conditions. This is greatly beneficial as it aids in understanding the nuances of complicated behavior while being able to test its causal relations to the conditions of the network.


Methodology: 10% of your grade. The methodology section should clearly explain how your experiments were conducted. What tools were used? Why did you choose to use these tools, and how do you know they are sound? What were the key parameters/variables/settings used during the experiments? Why did you choose these values?

I used ns-2 to generate the trace file dumps. These files were then parsed into python objects for ease access. The objects were merely wrappers for the datagrams within the trace file.  The packets were then encapsulated within a simulation object which allowed for further abstraction away from the trace dumps.  From here I constrcuted functions to determine the throughput, latency, and droprate of various packet streams.  Troughput was calculated as bytes per second, latency was calculated in seconds, and the drop rate was determined by the total packets lost over time. The graphs used were built by accumulating statistics within a delta amount of seconds. For drop rate, the delta was set to a relatively high number to match the relatively low drop rates, this was 0.5 seconds. Latency and throughput required a smaller delta and was set at 0.1 second. For the goals of the expirment this was sufficient but if I were to continue further analysis I would rectify this approach in various ways.


Results for Experiment 1: 30% of your grade. Present and thoroughly analyze the results from the first set of experiments. Explain why the results are the way they are by discussing how the different TCP variants react to the presence of congestion. Does each variant behave the same way, and if not, why not?

Congestion, 
at low cbr all four agents behave very simliar to each other
 reno
  heavy penality when CC kicks in at 8 and 9 mb cbr
 newreno
  quicker ramp up after CC compared to reno
 vegas
  finds a nice throughput quickly but undercuts potential on high utility networks
 tahoe
  more consistent then newreno though cc is painful

which TCP variants are able to get higher average throughput?
  It depends on the CBR. At 8mb CBR out of a 10mb pipe vegas was able to maintain
  a surprisingly high average at .72 Mb/s. A full .1 Mb/s over new reno. 
  Tahoe, reno, and new reno behave simliarly with new reno beating the two previous incarnations in all brackets.
  closing in a win over the 
Which has the lowest average latency?
  The data says tahoe but I doubt this.

Which has the fewest drops?
  Vegas had the fewest drops.

Is there an overall "best" TCP variant in this experiment, or does the "best" variant vary depending on other circumstances? 
  Vegas would be the winner if it didnt have such high latency and behave poorly when the netowork is at 90% usage. If low latency is a necessity and the network has high utlization new reno may be better choice.


Results for Experiment 2: 30% of your grade. Thoroughly and carefully present the results from the two-TCP stream experiments. When there are two TCP streams, do they share bandwidth fairly, and if not, why not? If there are any unexpected or "shocking" findings, highlight them in your text and discuss what leads to these results.

reno/reno
 frantic at high cbr
newreno/reno
 high cbr new reno dominates reno
 phasic behavior at lower cbr
vegas/vegas
 phasic at high and low cbr
 at mid level range one agent dominates other surprisingly
newreno/vegas
 new reno beats vegas ever so slightly

are the different combinations of variants fair to each other?
Are there combinations that are unfair, and if so, why is the combination unfair?

 No, especaially at certain network utilization levels. In my expiriments vegas was unfair to itself on a network of 7mb CBR. Similiar competitive behavior was obsvered with reno reno at high network utilzation though there was no persistent dominator in this situation.
 New reno beats out vegas across all CBR.

To explain unfairness, you will need to think critically about how the protocols are implemented and why the different choices in different TCP variants can impact fairness. 


Conclusion: 5% of your grade. Restate the significance of your study and highlight key results. Discuss the real-world significance of your results, and what the implications may be on deployed systems. Highlight any open questions that may motivate future studies.

key results:
  tpc is a hell of a protocl

real world significance:
  understanding congestion and fairness allows for better protocol design to increase reliability and utilization.

deployed implications:
  protocols should be used based upon previos knowledge of known network conditions.

open questions:
  other agents
  high RTT was not investigated
  heavy reordering

