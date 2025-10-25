# HARD FILTERS TABLE

Column Header,User Input/Requirement,Rationale
Price,User's maximum and minimum budget.,"Non-negotiable. If a mouse is outside the user's budget, it should not be recommended."
Connectivity,"User specifies ""Wired"" or ""Wireless"".",Non-negotiable. This is a fundamental preference for setup and performance.
Hand compatibility,"User specifies ""Right"" (for ergonomic) or ""Ambidextrous"" (for symmetrical).",Non-negotiable. A left-handed user will not want a right-hand-only ergonomic mouse.
Thumb rest / Ring finger rest,User specifies a preference for these comfort features.,"Highly recommended as a filter. A user who demands a thumb rest (e.g., on a large ergonomic mouse) will not be satisfied without one."
Size,"User specifies a size preference (e.g., Small, Medium, Large).","Highly recommended as a filter. A user with very large hands will not be happy with a ""Small"" mouse, regardless of other features."


# VECTOR EMBEDDINGS FEATURE TABLE

Column Header,Rationale / Relationship to User Input
Hump placement,"Directly ties to Grip Type (as you noted): Back (Claw), Center (Fingertip/Palm), Front (Palm). The closer the vector match, the better the fit."
Shape,"Symmetrical vs. Ergonomic. While Hand compatibility can filter, including the shape type in the vector helps match the user's general comfort preference."
"Length (mm), Width (mm), Height (mm)","These physical dimensions (especially when compared to the user's hand size, if collected) are critical for comfort and should be weighed heavily by the embedding."
Weight (grams),A major preference point (ultralight vs. heavier). The model can find a mouse closest to the user's target weight.
"Polling rate (Hz), Tracking speed (IPS), Acceleration (G), DPI","These are Performance metrics. A user specifying a need for ""high-performance"" will vector-match to mice with higher values in these fields."
"Side buttons, Middle buttons",Users with more complex needs may vector-match to mice with higher button counts.
Switches / Switches brand / Scroll wheel encoder,"A user might specify a desire for ""light and crisp clicks"" or mention a specific component, which the model can match using these descriptive fields."
Name / Model / Brand,Provides context and helps if the user searches for a style or a specific brand they've enjoyed before.