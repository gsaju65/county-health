# Written explanation

**What I chose** 
I built an infographic from the CDC PLACES 2025 county-level estimates. I started with one broad idea, that access to care and chronic disease are linked and narrowed it to two questions I could actually answer with this data:
1. Do counties where it is harder to get care carry more chronic disease?
2. What kind of counties face the most barriers, and where are they?

**Who is this for** 
I wrote this for general readers and for people who make decisions at the county or state level. Most of the health-policy conversation happens nationally, but care is delivered county by county, and the counties with the most barriers are small enough to disappear inside a national average.

**How the numbers were made** 
I picked five access measures (uninsured, no dental visit in the past year, no reliable transportation, food insecurity, housing insecurity) and five disease measures (diabetes, high blood pressure, coronary heart disease, obesity, fair or poor general health). Each one is a percentage of adults but on a very different scale, so I converted each to a z-score across counties and averaged them into an access barrier score and a disease burden score. I then split counties into quartiles on the barrier score, using age-adjusted rates throughout. I originally had a sixth access measure, no routine checkup in the past year, but dropped it after checking it: counties with more disease have more checkups, not fewer, so it was measuring demand for care rather than a barrier to it.

**Findings** 
The first thing I checked was whether the two scores actually move together which they do. However, it is tighter than I expected (r = 0.88). What told me that it was not just one measure driving the result was that all five disease measures rise in the same order across the barrier quartiles. Diabetes is the clearest example. In the quartile of counties with the fewest barriers, the median county has a 9.0% diabetes rate. In the quartile with the most barriers, it is 13.7%, about 1.5x higher. Poor general health follows the same pattern, going from 16.0% to 25.9%, or 1.6x.

**Surprises** 
The biggest one is coverage. Three of my barrier measures (transportation, food, housing) are not published for every state, so eleven states dropped out completely: Texas, Florida, Tennessee, Kentucky, Pennsylvania, Colorado, Washington, Oregon, South Dakota, Wyoming, and Vermont. That is about 29% of the US population and it changes which counties land in each quartile. With Texas and Tennessee gone, "the South" in my results mostly means the Deep South. The second limitation is the data itself. PLACES values are model-based estimates, not direct measurements and the same demographic inputs feed both of my scores, so part of the correlation is built in by the model. I can say the two move together. I cannot say one causes the other.

**Limitations** 
Eleven states have no social-determinant estimates and are absent entirely:
- Texas
- Florida 
- Tennessee
- Kentucky
- Pennsylvania
- Colorado
- Washington
- Oregon
- South Dakota
- Wyoming 
- Vermont. 
This leaves out 29% of the US population and shapes which counties land in each quartile. The dataset's values are model-based estimates, not direct measurements and the same demographic inputs feed both scores, so part of the correlation
is built in. This would make this an association, not a cause.

**Ethical Implications**
These are county averages, so they say nothing about any one person. A high-barrier county still has healthy people in it. I also had to think about how the story lands, because the counties at the top of my barrier score are small, rural, and mostly in the South, and it would be easy to read the result as a judgment on those places. The finding is about the systems around them, like insurance markets, transit, and food access, not the people who live there. Finally, for counties that were never surveyed, the estimate is a prediction from who lives there, so some of the pattern reflects the model's assumptions about demographic groups rather than anything measured.

**Takeaway** 
Diseases are common where getting care is hard.