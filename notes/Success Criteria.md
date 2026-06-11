# Success Criteria for boot.dev

Because this is being done as a personal project, I want to write out a goal because I could probably play with these equations endlessly.

## Reuquirements from boot.dev

- Try to spend 20-40 hours on this project.
- [x] Use a programming language you're already familiar with.
- Commit your code to Git often, and push it up to GitHub.
- Create a README.md file for your project. It should explain to readers:
- What the project is, and what it does.
- How to clone and run it.
- It's okay (even encouraged!) to use third-party libraries! That said, make sure that some of the code that you wrote is doing something interesting. You don't want a razor-thin wrapper around a third-party library to be the only thing you've written.

### My thoughts

I'll commit once I have the rectangular stress object finished. I've been avoiding it because I'm having too much fun with the work itself and find creating the repo and getting it onto github an extremely frustrating process. I'll be better after that.

README.md I'll add at the end. I also want to see if AI can generate a decent one.

I want this to be a pypl package so I'll have some additional things. Probably use an agent to help me set this up because it is not technically part of the project requirements.

## Choose an Idea from boot.dev:

The whole point of a personal project is that it's personal. The idea needs to be yours. It's time to fly closer to the sun and break out of tutorial hell, even if the project you build is simple for now, at least it's yours.

Build something that you find interesting.

This probably isn't a project that will make its way onto your portfolio or resume, but it's still good to get into the habit of building things that are interesting and useful. Interesting and useful projects have many benefits:

- They're more fun to work on
- They have more interesting and difficult problems to solve
- You (or someone else) might actually use them
- They're more likely to grab the attention of other people
- Attention from other people can lead to career opportunities

### My Thoughts

This is definitely personal and I have wanted to dig into subsurface loads and Poulos and Davis for years.

It will probably be on my resume and personal website when I set it up.

It will definitely be useful to me working with Rhino. Likely useful to others in this space and I could see Dane Parks using it.

## Success Criteria

So what would I actually consider successful enough to submit as my boot.dev project?

Not sure if I want to include the ad-hoc method. It is useful, but I think I'll be well above the 20 hour minimum listed in the spec of the personal project.

I want to have looked implimented:

1. [x] Rectangular load
2. Point load
3. Strip Load
4. Adding loads together
5. Notebook for rectangular load
6. Notebook for point load
7. Notebook for strip load
8. Notebook for adding loads together
9. Answer some questions (listed below)
10. Make this pip-installable.

### Ignore for boot.dev:

1. Impliment the AASHTO Ad-hoc method.
2. Include multiple lanes with an input for minimum adjacent wheel spacing.
3. Create a notebook exploring the ad-hoc method that I could send to the CANDE developer.
4. Include a function to account for pavement thickensses.

### Questions for the Elastic methods:

1. How should the singularity be addressed in the point load application?
2. How much of a difference does the rectangular distribution even make?
3. (Ignore for boot.dev)How much of a difference is there between the rectangular and strip methods?
4. (Ignore for boot.dev)Could you approximate the rectangular method with a grid of point methods? The rectangular method conservatively (for most applications) assumes a poisson's ratio of 0.50 so a grid of point loads would be useful for more realistic poisson's ratios.
5. [x] How should the radial stress be addressed for the point load?

### Questions for the Ad-hoc method (Ignore for boot.dev):

1. I think there is a zone where including pavement actually reduces the transverse distribution width and results in higher stresses. Can I plot that?

## Future Ideas:

1. The original idea of this was to compare ad-hoc and elastic methods with FEM results. Can I parametrically generate opensees models with brick elements to compare these?
2. What would the results look like? How do elastic, ad-hoc, and FEM results all look together on important questions such as those below?
3. Could using this library become a website? Parametric 3D models with automatic analysis seems useful.
4. How big of a role does Poisson's ratio play?
5. Cerutti - concentrated horizontal load
6. Stip horizontal loading

### FEM Results Questions:
    
1. Is plane-strain a good approximation?
2. How good of an approximation is ad-hoc method? Should it be refined?
