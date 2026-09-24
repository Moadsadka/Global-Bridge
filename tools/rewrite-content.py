#!/usr/bin/env python3
"""Rewrite the template's wellness copy as Global Bridge VIP travel copy.

The pages are a Framer export: one machine-generated HTML file per route, with
the same strings repeated for each responsive variant. Editing them by hand is
not reviewable, so every content change lives here instead. Re-running this
against a fresh export reproduces the site.

Four kinds of replacement, applied in this order:

  WORD_SPLIT  headings Framer splits into one animated <span> per word. The
              run of spans is rebuilt so a new heading need not have the same
              number of words as the old one.
  MARKUP      headings with one word coloured by a nested <span>. Matched as a
              regex over the real markup so the accent span is carried across.
  NODE        short strings (names, labels, prices). Matched only as a whole
              text node, ">key<", because a bare substring replace on a short
              word corrupts longer words that contain it.
  TEXT        long, unique sentences, replaced literally everywhere they
              appear, which covers the duplicated responsive variants for free.

TEXT keys must be long enough to be unambiguous; anything shorter belongs in
NODE. main() enforces that and reports keys that matched nothing.
"""
import re
import pathlib
import sys

MIN_TEXT_KEY = 30

# --- headings split into per-word animated spans -----------------------------
WORD_SPLIT = {
    "Where lasting change begins.": "Where every journey begins.",
    "The signs that something needs to change.":
        "The friction that slows a principal down.",
}

# --- headings with a colour-accented word ------------------------------------
# (\1 is the opening tag of the accent span, kept as the template wrote it.)
MARKUP = [
    (r'>Guiding you back to (<span[^>]*>)balance\.</span>',
     r'>Every detail handled in \1advance.</span>'),
    (r'>You are (<span[^>]*>)not</span> alone in this\.',
     r'>Trusted with \1journeys</span> that cannot slip.'),
    (r'>Find the support that fits (<span[^>]*>)your</span> life\.',
     r'>An arrangement that fits \1your</span> schedule.'),
    (r'>You deserve to feel like (<span[^>]*>)yourself</span> again\.',
     r'>Tell us where you need to be \1next</span>.'),
    (r">>Hi, I'm (<span[^>]*>)Maya\.</span>".replace(">>", ">"),
     r'>This is \1Global Bridge.</span>'),
]

# --- whole text nodes --------------------------------------------------------
NODE = {
    # Calls to action
    "Begin Your Journey": "Request Arrangements",
    "How I Can Help": "Our Services",
    "Book a Call": "Request a Call",

    # Hero
    "Mind · Body · Lifestyle": "Valencia · Tripoli · Worldwide",

    # Hero statistics. Placeholders — real figures to come from the client.
    "300+": "24/7",
    "Hours of Coaching": "Coordination Desk",
    "200+": "3",
    "Client Sessions": "Regions Covered",
    "95%": "100%",
    "Report Reduced Stress": "Managed End to End",

    # About
    "About me": "About us",

    # Services
    "Stress &amp; Anxiety": "Private Aviation",
    "Burnout Recovery": "Executive Transfers",
    "Life Transitions": "VIP Airport Services",
    "Mindfulness Tech": "Business Concierge",

    # Testimonials. Attributions are placeholders — real, attributed client
    # quotes must replace these before launch.
    "Real stories": "Client confidence",
    "Sarah Silos": "Managing Director",
    "Alex Morgan": "Chief of Staff",
    "Elena Azalea": "Executive Assistant",
    "James Wilson": "Chief Executive",
    "Mika Wazowski": "Group Director",
    "Priya Patel": "Founder",
    "Marketing Director": "Private investment office",
    "Startup Founder": "Family office",
    "Freelance Designer": "Energy sector",
    "Sales Manager": "Industrial group",
    "Nurse": "Trading company",
    "Featured in": "Trusted by",

    # Engagements
    "Programs": "Engagements",
    "Group Program": "Per Journey",
    "Calm Collective": "Single Journey",
    "$899": "By arrangement",
    "8 Weekly Group Calls (Max 6 People)": "Dedicated journey coordinator",
    "Private Community Access": "Private aviation and charter booking",
    "Two 1:1 Check-Ins": "Airport fast-track at both ends",
    "Meditation Library": "Chauffeured transfers throughout",
    "Weekly Exercises": "Accommodation arranged and confirmed",
    "3 Months Extended Access": "Full itinerary documentation",
    "1:1 Premium": "Retainer",
    "Reset &amp; Restore": "Annual Retainer",
    "$2,999": "By arrangement",
    "12 Weekly 1-Hour Sessions": "Unlimited journeys within the year",
    "Personalized Toolkit": "Named coordinator on call at any hour",
    "Custom Meditation Recordings": "Standing preferences held on file",
    "Weekday Text Support": "Priority access to aircraft and suites",
    "Sustainability Plan": "Close protection arranged on request",
    "Lifetime Session Recordings": "Quarterly travel review and reporting",

    # How it works
    "Meet &amp; Connect": "Tell Us",
    "Work Together": "We Arrange",
    "Feel Like You Again": "You Travel",

    # Questions
    "How much does it cost?": "How is this priced?",

    "Written by Maya": "Written by Global Bridge",

    # Footer
    "Twitter": "LinkedIn",
    "Meta": "Email",
    "Created by Hamza Ehsan": "Valencia · Tripoli",

    # Journal author
    "Maya": "Global Bridge",
}

# --- long, unique strings ----------------------------------------------------
TEXT = {
    # Page identity
    "Holistic - Wellness &amp; Coaching Website Template for Framer":
        "Global Bridge — VIP Business &amp; Travel Services",
    "Holistic is a premium Framer template built for wellness coaches, therapists, and holistic practitioners who want to look established, attract clients, and book sessions from day one.":
        "Global Bridge arranges private aviation, executive transfers and business concierge for principals travelling between Europe, North Africa and the Gulf.",

    # Hero
    "Compassionate, evidence-based wellness coaching for stress, anxiety, and burnout.":
        "Private aviation, executive ground transport and business concierge for principals moving between Europe, North Africa and the Gulf.",

    # The friction list
    "You're tired all the time but you can't switch off":
        "Commercial terminals and public queues on every leg",
    "You're holding it all together but quietly falling apart":
        "Chasing three suppliers to assemble one itinerary",
    "Successful on paper but something still feels deeply off":
        "Briefing a new driver in every city you land in",
    "Self-help books and meditation apps just aren't cutting it":
        "Hotels that cannot hold a suite at short notice",
    "Resting feels wrong, like you should be doing more":
        "Itineraries that circulate beyond your own office",
    "You know something needs to change but can't start":
        "A transfer that runs late and misses the aircraft",

    # About
    "I help overwhelmed professionals find their way back to themselves.":
        "We arrange travel for people whose time cannot be wasted.",
    "Five years ago, I was pulling 60-hour weeks and living on coffee, totally convinced I had it all figured out. Then my body had other ideas. Panic attacks, couldn't sleep, the whole mess.":
        "Global Bridge was founded to solve one problem: a principal's journey touching six suppliers, none of whom talk to each other. Aircraft, ground transport, airport formalities and accommodation are arranged by one team, on one itinerary.",
    "I've been there, and I know how isolating it feels. Now I help people find their way back to feeling like themselves again.":
        "We work from Valencia and Tripoli, across Europe, North Africa and the Gulf. Every arrangement is handled with the privacy and precision our clients' schedules demand.",

    # Services
    "Four key areas where gentle guidance and proven techniques create lasting transformation.":
        "Four services that together cover every stage of a journey, from departure to return.",
    "Gentle practices to calm your mind, ease tension, and bring you back.":
        "Private jet charter, VIP terminal access and flight coordination arranged around your schedule.",
    "Rebuild your energy and rediscover your purpose without burning it all down.":
        "Chauffeured luxury vehicles for every leg, from hotel to terminal to meeting and back.",
    "Support through career shifts, loss, and the in-between moments.":
        "Fast-track immigration, baggage assistance and discreet departure procedures at both ends.",
    "Practical techniques you can actually use, even on your worst days.":
        "Accommodation, meeting coordination and executive assistance throughout your engagements.",

    # Testimonials
    "Hear from others who've made the journey from overwhelmed to feeling like themselves again.":
        "How the offices and executives whose travel we manage describe working with us.",
    "I used to lie awake replaying work conversations. Now I actually sleep through the night. Maya helped me find calm in the chaos.":
        "Four cities in six days and not one arrangement needed my attention.",
    "I was drowning in stress from travel and deadlines. Maya's simple breathing techniques changed everything.":
        "The car was waiting before we had cleared the aircraft steps.",
    "Going through my divorce felt impossible while managing everything else. Maya helped me rebuild my confidence and create space for what truly mattered in my life which helped both myself and my family.":
        "A schedule changed at midnight and the aircraft, the driver and the hotel had all moved before morning.",
    "I used to feel guilty taking breaks. Maya showed me that rest isn't laziness, it's necessary for creativity and focus.":
        "They understand that discretion is the service itself. Nothing left their desk.",
    "I thought burnout was just part of entrepreneurship. Maya taught me that boundaries actually make you more effective.":
        "One number to call, and the whole itinerary is handled from there.",
    "Maya's techniques actually work during crazy busy days at the office. I finally have practical tools that fit into real life, not just theory.":
        "Fifteen years of travel and this is the first time I stopped checking.",

    # Engagements
    "Choose from different ways to work together, designed to meet you wherever you are in your journey.":
        "Two ways to work with us, depending on how often you travel.",
    "Learn alongside others while receiving individual guidance tailored to you.":
        "One journey arranged end to end, from the first transfer to the last.",
    "Deep, personalized work to completely transform your relationship with stress.":
        "Continuous coverage for principals and teams who travel constantly.",

    # How it works
    "An honest conversation about what's really going on.":
        "One call or message with the dates and the destination.",
    "Identifying patterns and designing practices that fit your life.":
        "Aircraft, transfers, accommodation and everything in between.",
    "Moving through days with intention instead of survival mode.":
        "You arrive, and nothing along the way needs your attention.",

    # Questions
    "Do I need technical knowledge to work with you?": "How much notice do you need?",
    "No. We handle all the technical work from start to finish. You just need to share how your business operates, and we take care of the rest.":
        "We prefer several days, but we regularly arrange complete itineraries within twenty-four hours. Tell us the constraint and we will tell you honestly what is possible.",
    "How long does it take to see results?": "Which regions do you cover?",
    "Most clients see measurable results within 45 days. We focus on quick wins first, then build on that foundation over time.":
        "Europe, North Africa and the Gulf are handled directly from our Valencia and Tripoli offices, and the rest of the world through partners we have worked with for years.",
    "What if the automation doesn't work for my business?": "How do you handle confidentiality?",
    "We start with a thorough assessment to ensure automation makes sense for your specific workflows. If something isn't working, we refine it until it does.":
        "Your itinerary is held by the coordinator assigned to you and is not circulated further. We work with principals whose movements are sensitive, and treat that as the service itself.",
    "Pricing depends on your needs and scope. After our free assessment, we'll provide a clear proposal with transparent pricing and no hidden fees.":
        "Every journey is quoted individually, because no two use the same aircraft, vehicles or hotels. Retainer clients agree rates in advance.",
    "What happens after implementation?": "What if plans change mid-journey?",
    "We provide training for your team and ongoing support to ensure everything runs smoothly. As your business evolves, we help optimize and refine your systems.":
        "Your coordinator is reachable at any hour and rearranges the remaining legs around you. Changes in the air or overnight are routine.",

    # Closing call to action
    "Book a free discovery call and let's talk about what's weighing you down.":
        "Send us the dates and the destination. We arrange everything in between.",

    # Footer
    "© 2026 Holistic. All rights reserved.":
        "© 2026 Global Bridge. All rights reserved.",
}

# --- inner pages -------------------------------------------------------------
# About, Services, Contact, Journal and 404 carry their own copy. Same four
# mechanisms, kept separate so the home page above stays readable.

WORD_SPLIT.update({
    "It started and ended with burnout.":
        "It began with one missed connection.",
    "Guiding you back to balance.": "Every detail handled in advance.",
    "Let's have a conversation.": "Tell us where you are going.",
    "Writing from the other side of burnout.": "Notes from the travel desk.",
    "You wandered off the path.": "This page has moved on.",
})

MARKUP += [
    # About
    (r">You don't need fixing, you need (<span[^>]*>)support\.</span>",
     r'>Not a list of suppliers, but a \1plan.</span>'),
    (r'>The stuff that actually (<span[^>]*>)matters\.</span>',
     r'>The principles behind every \1arrangement.</span>'),
    (r'>The qualifications that (<span[^>]*>)behind</span> the work\.',
     r'>The network standing \1behind</span> the desk.'),
    # Services
    (r'>Four areas with (<span[^>]*>)one approach\.</span>',
     r'>Four services, \1one desk.</span>'),
    (r">This isn't a quick fix\. It's a proper (<span[^>]*>)reset\.</span>",
     r'>Nothing about a journey is \1improvised.</span>'),
    # Contact
    (r'>Pick a time that works (<span[^>]*>)for you\.</span>',
     r'>Pick a time that suits \1your day.</span>'),
    (r'>Or send me a (<span[^>]*>)message\.</span>',
     r'>Or send us a \1message.</span>'),
]

NODE.update({
    # Page titles
    "About - Holistic": "About - Global Bridge",
    "Services - Holistic": "Services - Global Bridge",
    "Contact - Holistic": "Contact - Global Bridge",
    "Page Not Found - Holistic": "Page Not Found - Global Bridge",

    # About
    "How I Work": "How we work",
    "Backed by research": "One point of contact",
    "No judgement, ever": "Discretion by default",
    "The whole picture": "The whole journey",
    "What I Believe": "How we operate",
    "The truth, but gently": "Say what is possible",
    "Small shifts beat big overhauls": "Plan for the change",
    "Your life, your pace": "Standing preferences",
    "Rest isn't lazy": "Reachable at any hour",
    "Training": "Reach",
    "2019": "Valencia",
    "Holistic Health Coach": "European operations",
    "Institute for Integrative Nutrition": "Charter, transfers and Schengen formalities",
    "Certified": "Direct",
    "2020": "Tripoli",
    "Stress Reduction (MBSR)": "North African operations",
    "UMass Medical School": "Ground, security and airport liaison",
    "2021": "Gulf",
    "Nutrition Practitioner": "Partner network",
    "National Academy of Sports Medicine": "Doha, Dubai, Riyadh and Abu Dhabi",
    "2022": "Worldwide",
    "Trauma-Informed Care": "Extended network",
    "Somatic Experiencing International": "Operators we have worked with for years",

    # Services
    "What I help with": "What we arrange",
    "Nervous system regulation": "Aircraft sourced to the route",
    "Breathing and grounding techniques": "VIP terminal and private lounge access",
    "Sustainable stress management": "Slots, permits and handling arranged",
    "Burnout recovery": "Executive transfers",
    "Rest and recovery planning": "Vetted chauffeurs in every city",
    "Boundary setting": "Armoured and escorted options",
    "Rebuilding sustainable routines": "Timed to the aircraft, not the clock",
    "Life transitions": "VIP airport services",
    "Navigating uncertainty": "Fast-track immigration and customs",
    "Identity and confidence rebuilding": "Met at the aircraft steps",
    "Creating stability in change": "Baggage handled without you present",
    "Mindful living": "Business concierge",
    "Daily habits and routines": "Suites held and confirmed in advance",
    "Healthy boundaries": "Meeting rooms and interpreters",
    "Intentional living practices": "Restaurants, security and local liaison",
    "What to expect": "How it runs",

    # Contact
    "Book a free session": "Speak to a coordinator",
    "Embed your calendar": "Booking calendar",
    "Discovery call": "Introductory call",
    "Free": "No charge",
    "Full session": "Planning call",

    # Journal
    "Burnout": "Planning",
    "Stress": "Ground",
    "Self-care": "Aviation",
    "Mindfulness": "Discretion",
    "Get new posts straight to your inbox.": "Get new notes straight to your inbox.",
})

TEXT.update({
    # About
    "I was a consultant working 60-hour weeks and calling it ambition. One morning I woke up and couldn't get out of bed. Not from exhaustion, from emptiness.":
        "Our founders spent years moving between Valencia, Tripoli and the Gulf, and watched the same failure repeat. One late car undid an itinerary that had taken weeks to assemble, because nobody owned the journey as a whole.",
    "I'd built the career, the house, the whole thing, and felt nothing. It took falling apart to figure out what actually mattered. Now I help other people skip the falling apart bit.":
        "Global Bridge exists so that ownership sits in one place. A single coordinator holds the aircraft, the vehicles, the airport formalities and the accommodation, and answers for all of it from departure to return.",
    "Most of the people I work with aren't broken. They're stretched too thin and have been ignoring their own needs for years.":
        "Most principals are not short of suppliers. They are short of one person who can see the whole journey and is accountable for every part of it.",
    "No trendy recommendations. If the science isn't there, it's not here.":
        "One coordinator holds your itinerary end to end. You never repeat yourself to a second person.",
    "You can say the real thing here. I'm not here to lecture you.":
        "Your movements stay with the people arranging them, and are not circulated further.",
    "Sleep, stress, food, work, relationships. It's all connected.":
        "Aircraft, transfers, formalities and hotels, arranged together rather than separately.",
    "I've learned these the hard way over eight years of doing this work, and they guide every session I run.":
        "Four rules that decide how every journey is planned and how every change is handled.",
    "I'll always be straight with you. Not harsh, but real. That's how things actually change.":
        "If a schedule cannot be met safely or legally, we say so at once and offer the nearest alternative. We do not promise and then improvise.",
    "Nobody sustains a complete life makeover overnight. We start small and build from there.":
        "Every itinerary is built with the next aircraft, car and room already held in reserve, so a delay costs minutes rather than the whole day.",
    "I'm not here to hand you a generic plan. Everything we do is built around how you actually live.":
        "Seat, vehicle, suite, catering and timing are recorded once, applied to every journey, and never asked for twice.",
    "You've probably been told to push through. I'm telling you to stop. That's where the real work begins.":
        "Your coordinator answers through the night and across time zones. A journey in progress is never left to an inbox.",
    "Over 300 hours of formal training and eight years of working with real people going through real things.":
        "Offices in Valencia and Tripoli, and vetted operators in every region we send clients through.",

    # Services
    "I work with people dealing with stress, burnout, and the feeling that something needs to change but they're not sure where to start.":
        "Private aviation, ground transport, airport formalities and accommodation, arranged for principals whose schedules leave no room for error.",
    "You don't need to fit into a box. Most of the people I work with are dealing with a mix of these.":
        "Most journeys use all four. They are arranged together, by the same coordinator, on a single itinerary.",
    "When your mind won't switch off and your body's stuck in fight-or-flight. We work on calming your nervous system and building a life that doesn't constantly overwhelm you.":
        "Private jet and helicopter charter, VIP terminal access and flight coordination, arranged around your schedule rather than a published one.",
    "You pushed too hard for too long and now you're running on empty. We rebuild from the ground up, starting with rest and working toward a routine that doesn't break you again.":
        "Chauffeured vehicles for every leg, from residence to terminal to meeting and back, held to the same standard in every city.",
    "Career changes, relationship shifts, becoming a parent, moving countries. The big life moments that leave you feeling unsteady. We work through the adjustment together.":
        "Fast-track immigration, baggage handling and discreet arrival and departure procedures at both ends of every flight.",
    "For people who want to be more intentional about how they live. We look at habits, routines, and boundaries so you actually enjoy your days instead of just getting through them.":
        "Accommodation, meeting coordination and executive assistance for the part of the journey that happens on the ground.",
    "I won't give you a checklist and send you on your way. Every session is a real conversation about where you're at and what needs to shift.":
        "You give us the dates and the destinations. We return a single itinerary covering every leg, with the aircraft, vehicles and rooms already held.",
    "Between sessions, you'll have exercises and prompts to work through at your own pace. Nothing overwhelming, just enough to keep things moving.":
        "Through the journey your coordinator confirms each leg ahead of you, so the car is in place before the aircraft lands and the suite is ready before you reach it.",
    "If something isn't working, we change it. The plan works for you, not the other way around.":
        "When plans change, the remaining legs are rebuilt around you. That is routine, and it does not need your attention.",

    # Contact
    "Whether you're ready to book a session or just want to ask a question, this is the place. No pressure, no obligations.":
        "Whether you have a confirmed itinerary or just a date and a destination, this is the place to start. No obligation either way.",
    "Free 20-minute discovery calls. No commitment, just a conversation about where you're at.":
        "A twenty-minute call to go through your dates, your route and how you prefer to travel.",
    "Embed your calendar here so your visitors can pick a date, time, and book directly.":
        "Connect a booking calendar here so clients can choose a time and confirm it directly.",
    "I read every message personally and reply within 48 hours (usually less).":
        "Every message reaches a coordinator directly and is answered within a few hours.",

    # Journal
    "Honest writing about the things I see in my practice and the lessons I keep coming back to.":
        "Practical notes on private travel, drawn from the journeys we arrange.",
    "No spam, no fluff. Just honest writing when I have something worth sharing.":
        "No spam. A short note when we have something worth passing on.",
    "Holistic wellness coach helping overwhelmed professionals find their way back to balance. Based in California.":
        "Global Bridge arranges private aviation, executive transfers and business concierge from offices in Valencia and Tripoli.",

    # 404
    "That's okay. Finding your way back is kind of what we do here.":
        "Not a problem. Getting people where they need to be is what we do.",
})

# --- journal -----------------------------------------------------------------
# Six template articles about wellness, replaced with six about private travel.
# Each body is rewritten paragraph for paragraph so the same replacement also
# lands in Framer's hydration payload, where the article is repeated as JSON.

SLUGS = {
    "tired-vs-burned-out": "booking-vs-itinerary",
    "body-keeps-the-score": "ground-leg-breaks-journeys",
    "just-rest-is-terrible-advice": "charter-is-not-a-plan",
    "five-minutes-is-enough": "discretion-is-a-procedure",
    "boundaries-not-difficult": "saying-no-to-a-schedule",
    "stopped-counting-calories": "what-we-check-before-departure",
}

NODE.update({
    'The difference between tired and burned out - Holistic':
        'The difference between a booking and an itinerary - Global Bridge',
    "Your body keeps the score even when you're fine - Holistic":
        'The ground leg is where journeys break - Global Bridge',
    'Why "just rest" is terrible advice - Holistic':
        'Why "charter a jet" is not a plan - Global Bridge',
    "You don't need to meditate for an hour - Holistic":
        'Discretion is a procedure, not a promise - Global Bridge',
    "Setting boundaries doesn't make you difficult - Holistic":
        'When we say a schedule will not work - Global Bridge',
    'What I actually eat in a day - Holistic':
        'What we check the day before departure - Global Bridge',
})

TEXT.update({
    # ---- titles and excerpts (also appear on the index and in cross-links) --
    "The difference between tired and burned out":
        "The difference between a booking and an itinerary",
    "Everyone says they're burned out. But there's a real difference between needing a weekend off and needing to fundamentally change how you're living.":
        "Anyone can book a flight and a car. An itinerary is the plan that still holds when one of them slips.",
    "Your body keeps the score even when you're fine":
        "The ground leg is where journeys break",
    "Stress doesn't always look like stress. Sometimes it shows up as a stiff neck, a short temper, or a 3am wake-up you can't explain.":
        "The aircraft is rarely the problem. Almost every hour we see lost is lost between the door and the terminal.",
    'Why "just rest" is terrible advice': 'Why "charter a jet" is not a plan',
    "Rest isn't one thing. There are at least seven types, and most people are only getting one of them.":
        "Chartering is one decision out of seven, and the other six are the ones that decide whether the day works.",
    "You don't need to meditate for an hour":
        "Discretion is a procedure, not a promise",
    "The wellness industry makes mindfulness feel like a performance. It doesn't have to be. Here's what actually works for people with busy lives.":
        "Every travel company says it is discreet. The difference is whether anything about how they work makes it true.",
    "Setting boundaries doesn't make you difficult":
        "When we say a schedule will not work",
    "Most of my clients feel guilty about boundaries. Here's what I tell them.":
        "Telling a client their plan cannot be flown as written is the least popular part of the job.",
    "Tracking macros made me miserable. Here's the simpler approach that actually stuck.":
        "Not a long list. Just the handful of things that have actually gone wrong before.",

    # ---- booking vs itinerary ----------------------------------------------
    'Everyone uses the word "burnout" now. Had a long week? Burnout. Feeling a bit flat on a Monday morning? Burnout. Didn\'t feel like cooking dinner? Must be burnout.':
        "Everyone says their travel is arranged. A jet is booked, a hotel is confirmed, a car is ordered. Three arrangements sitting in three different inboxes.",
    "But there's a real difference between being tired and being burned out, and mixing them up can lead you down the wrong path entirely.":
        "But there is a real difference between a set of bookings and an itinerary, and treating one as the other is how a day comes apart.",
    "Tiredness has a cause and a cure. You stayed up too late, you had a demanding week, you've been running around after your kids all day. The fix is straightforward: sleep, rest, a weekend off. You bounce back.":
        "A booking has one supplier, one reference and one responsibility: to deliver that one thing at that one time. The charter company owes you an aircraft. The hotel owes you a room. Neither of them owes you the connection between the two.",
    "Tired people still care about things. They're just low on energy. They can still picture themselves feeling good again. They know what would help, even if they haven't done it yet.":
        "Bookings are not aware of each other. If the aircraft moves by two hours, the car does not know, the hotel does not know, and nobody tells the meeting at the other end.",
    "Burnout isn't about energy levels. It's about meaning. You could sleep for a month and still wake up feeling the same way because the problem isn't physical exhaustion. It's emotional and psychological depletion.":
        "An itinerary is the whole journey held by one person, with the dependencies written down. It records that the car has to leave forty minutes before the slot, that the handler needs the manifest by a certain hour, and that the suite is held under a name matching the travel document.",
    "When you're burned out, you stop caring about things that used to matter to you. Work feels pointless. Hobbies don't interest you. You go through the motions but there's nothing behind it. You might not even feel stressed anymore because you've gone past stress into numbness.":
        "It also carries the alternatives: a second aircraft identified for the route, a second vehicle in the city, a room held at a nearby property. None of them are used on most journeys, which is exactly why they cost so little to hold.",
    "The World Health Organisation actually classifies burnout specifically as an occupational phenomenon, but I see it show up in people's personal lives too. Parents, carers, people who've been putting everyone else first for years.":
        "The test is simple. If one element moves by two hours, does anybody have to be told twice?",
    "How to tell which one you're dealing with": "How to tell which one you have",
    "Ask yourself these two questions:": "Two questions settle it.",
    "If I took a proper two-week holiday with no responsibilities, would I come back feeling like myself again? If the answer is yes, you're probably tired. Rest will fix it.":
        "If tonight's departure slipped by three hours, how many people would have to be called? If the answer is more than one, you have bookings.",
    "Can I still picture a version of my life that excites me? If the answer is no, if everything feels flat regardless of circumstances, that's closer to burnout.":
        "If the destination changed tomorrow, who rebuilds the rest of the week? If the answer is you or your assistant, you have bookings.",
    "The reason I care about this distinction is because tired people and burned out people need completely different things.":
        "The difference only becomes visible on the day something goes wrong, which is precisely the day it is too late to build.",
    "If you're tired, you need rest and maybe some better boundaries around your time. If you're burned out, rest alone won't fix it. You need to look at the underlying patterns that got you here: the people-pleasing, the overworking, the complete absence of anything in your life that's just for you.":
        "Bookings are cheaper to make and more expensive to hold together. The cost is paid in an assistant's evening, a missed slot, a meeting pushed to the following day.",
    "I've had clients come in saying they're burned out when they're actually just exhausted from a rough patch. And I've had clients insist they just need a holiday when they're clearly dealing with something much deeper.":
        "We see offices with excellent suppliers and no itinerary, and offices with an ordinary supplier list and a very good one. The second travels better.",
    "Getting the diagnosis right matters because it changes everything about what you do next.":
        "Getting this right changes what a journey costs you in attention, which is usually the only budget that matters.",

    # ---- the ground leg ------------------------------------------------------
    "You might think you're handling stress well. You're still getting to work, still ticking things off the list, still showing up. But your body has a different opinion.":
        "You might think the aircraft is the risky part of a journey. It is the expensive part, the visible part, the part the whole plan is built around. It is almost never the part that fails.",
    "Stress doesn't always announce itself with panic attacks and breakdowns. Most of the time it's quieter than that. It shows up in your body long before it shows up in your mind.":
        "Delay does not usually announce itself on the runway. Most of the time it is quieter than that, and it happens on a road, in a queue, or at a desk.",
    "A stiff neck that won't go away no matter how much you stretch. A jaw that's clenched when you wake up in the morning. Stomach issues that your GP can't find a cause for. Waking up at 3am for no apparent reason. A short temper that seems to come out of nowhere.":
        "A driver who does not know which gate a private terminal uses. A vehicle sent to the main terminal instead of the general aviation side. Twenty minutes at a desk because a name was filed with a different spelling. A road closed for an event that nobody checked.",
    "These aren't random. They're your nervous system telling you something is off.":
        "None of these are exotic. They are the ordinary failures of a leg that nobody owned.",
    "I had a client once who came in for help with insomnia. She was convinced it was a sleep problem. We spent the first session talking about her life and within twenty minutes it was obvious: she was carrying an enormous amount of unprocessed stress from a job she hated and a relationship she was avoiding dealing with. The insomnia wasn't the problem. It was the symptom.":
        "We once took over for a client whose charter had been arranged impeccably and whose day was still lost, because the car meeting them had been booked by a hotel concierge who had never been to that terminal. Forty minutes driving the perimeter fence. The aircraft was never the problem.",
    "Your nervous system doesn't lie": "Ground is harder than air",
    "Here's the thing about your body: it doesn't have the ability to rationalise. Your brain can tell itself \"I'm fine, this is manageable, other people have it worse.\" Your body can't do that. It just responds to the signals it's receiving.":
        "Aviation is heavily proceduralised. Slots, handling, crew duty and permits are written down, and the people doing the work do it the same way every time, in every country.",
    "When you're under chronic stress, your nervous system stays in a state of low-level activation. Not full fight-or-flight, but not properly at rest either. You're stuck in this middle ground where everything technically works but nothing feels easy.":
        "Ground transport is not. Standards vary by city, by operator and sometimes by individual driver. The same company can be excellent in one capital and unreliable two hours down the coast.",
    "Over time, this shows up as tension, digestive problems, poor sleep, low immunity, and that general feeling of being wired but tired at the same time.":
        "Over time it produces the same complaint: everything was arranged, and it still took all day.",
    "The first step is honestly just paying attention. Most people have completely disconnected from their physical experience. They live in their heads and only notice their body when something hurts badly enough to force attention.":
        "The first step is naming the person. Every ground leg has a named operator and a named driver, confirmed the day before, rather than a dispatch queue that assigns somebody on the morning.",
    "Start checking in. Not in a complicated meditation way, just a simple \"where am I holding tension right now?\" a few times a day. You'll be surprised what you find.":
        "The second is the gate. Which entrance, which terminal and which apron the vehicle uses is confirmed in writing with the handler, for every airport on the itinerary.",
    "The second step is understanding that you can't think your way out of a body-based stress response. Telling yourself to relax doesn't work because relaxation isn't a cognitive process. It's a nervous system process. You need tools that work with the body directly: breathing, movement, touch, time in nature.":
        "The third is timing against the aircraft rather than against the clock. The car is scheduled off the slot, so when the slot moves the vehicle moves with it and nobody has to make a call.",
    "I'm not saying don't also address the root causes of your stress. Obviously do that. But while you're working on the bigger picture, your body needs attention too. It's been carrying the load for longer than you think.":
        "None of this removes traffic or weather. It removes the failures that were avoidable, which in our experience are most of them.",

    # ---- charter is not a plan ----------------------------------------------
    "Whenever someone tells me they're exhausted, the first piece of advice they've usually already received is \"you just need to rest.\" And look, it's not wrong exactly. But it's not helpful either, because it assumes rest is one thing. It's not.":
        "When someone needs to be in three cities in a week, the advice they have usually already had is \"charter a jet.\" It is not wrong exactly. It is just incomplete, because chartering is not one decision. It is seven.",
    "Most people think of rest as sleep or lying on the sofa doing nothing. And yes, those are forms of rest. But they're only two out of at least seven types that your body and mind actually need.":
        "Most people think of a charter as a booking: pick an aircraft, agree a price, turn up. That is one of the seven things that decide whether the day works.",
    "Dr Saundra Dalton-Smith identified seven types of rest, and when I came across her work it changed how I approach recovery with every single client.":
        "The other six are less visible, and each of them has ended a schedule that looked perfectly sound on paper.",
    "Physical rest is the obvious one. Sleep, naps, letting your body recover. But even this has two sides: passive (sleeping) and active (stretching, yoga, massage).":
        "The aircraft. Range and cabin measured against the real route, not the marketing one. A light jet that needs a fuel stop turns a four-hour day into six.",
    "Mental rest is what you need when your brain won't stop. When you're lying in bed but your mind is running through tomorrow's to-do list. Mental rest means creating breaks in your thinking throughout the day, not just at bedtime.":
        "The airport. Two airports serving the same city can be forty minutes apart on the ground and very different on handling. The closer one is not always the faster one.",
    "Emotional rest is the freedom to be honest about how you're feeling. If you spend all day performing \"I'm fine\" for other people, you're not getting emotional rest even if you're sleeping eight hours.":
        "The slot. Congested airports allocate departure and arrival windows, and missing one costs hours rather than minutes.",
    "Social rest means time away from people who drain you and time with people who fill you up. Or just time alone. Not all socialising is equal and not all alone time is restful.":
        "The permits. Overflight and landing permission for some jurisdictions takes days rather than hours, and a route that avoids them is often worth more than a faster aircraft.",
    "Sensory rest is a break from stimulation. Screens, noise, bright lights, notifications. Your nervous system needs periods of low input to recover.":
        "The handling. Somebody on the ground has to meet the aircraft, move the baggage and clear the passengers. Whether that is arranged decides how long the last two hundred metres take.",
    "Creative rest is exposure to beauty and inspiration without the pressure to produce anything. A walk in nature, visiting a gallery, listening to music. Input without output.":
        "The crew. Duty limits are legal limits. A crew out of hours cannot fly you whatever the charter costs, so a long day has to be built around them before it starts.",
    "Spiritual rest is connection to something larger than yourself. Purpose, meaning, community. It's the feeling that what you're doing matters in some way.":
        "The alternative. What happens if the aircraft goes technical at seven in the evening. Either there is an answer already identified, or there is a night in an airport hotel.",
    "When a client comes in saying they're exhausted and they're sleeping nine hours a night, the answer isn't more sleep. The answer is figuring out which type of rest they're actually missing.":
        "When a client asks for a jet and is quoted a price in ninety seconds, the other six decisions have not been made. They have been deferred to the day of travel.",
    "Usually it's emotional or social rest. They're surrounded by people but performing all day. They're never actually being themselves in a space that feels safe. And no amount of sleep fixes that.":
        "Most of the time nothing goes wrong and the deferral costs nothing. The value of making those decisions in advance is entirely in the days when something does.",
    "So next time someone tells you to \"just rest,\" ask yourself: which kind? That question alone can shift everything.":
        "So when somebody says \"just charter a jet\", the useful question is which of the seven they have covered. That question alone usually changes the plan.",

    # ---- discretion ----------------------------------------------------------
    "I'll be upfront: I'm a meditation advocate. I recommend it to almost every client I work with. But the way the wellness industry talks about meditation makes most people feel like they're already failing before they start.":
        "We will be direct: every company in this business says it is discreet. It appears on every website, ours included, and on its own it means nothing at all.",
    "Somewhere along the line, meditation became another thing to optimise. People ask me what app they should use, how long they should sit for, whether they're doing it \"right.\" They've turned a practice that's supposed to reduce pressure into another source of it.":
        "Discretion has become a marketing word. Clients are told their privacy is respected, their details are safe and their movements are confidential, and not one of those sentences describes anything anybody actually does.",
    "I've had clients tell me they tried meditation and it \"didn't work.\" When I ask what happened, they say they sat for twenty minutes, couldn't stop thinking, felt frustrated, and gave up. That's not meditation failing. That's expectations failing.":
        "We have taken on clients whose arrangements leaked constantly, not through malice but through ordinary process. Itineraries in group email threads. Drivers given the passenger's name and employer because a booking form asked for them. Hotel reservations on a company account visible to a dozen people.",
    "Meditation isn't about emptying your mind. It never was. It's about noticing what's happening in your mind without getting pulled into it. That's it.":
        "Discretion is not silence. It is deliberately limiting who holds which piece of information, so that no single supplier ever has the whole picture.",
    "You sit, you breathe, thoughts come, you notice them, you come back to your breath. The thoughts aren't the problem. The noticing is the practice. Every time you catch yourself drifting and come back, that's a rep. That's the thing working.":
        "The driver needs a time, a pickup point and a destination. The handler needs the manifest. The hotel needs a name and a card. None of them needs the purpose of the journey, the other legs, or who else is travelling. Withholding that is not rudeness. It is the job.",
    "The research on this is actually quite clear. Consistent short sessions outperform sporadic long ones. Five minutes every day does more for your stress levels, focus, and emotional regulation than a 30-minute session once a week.":
        "One coordinator holds the complete itinerary. Every supplier receives only their own leg, in a message addressed to them and nobody else. There is no group thread containing the journey.",
    "And five minutes is manageable. Nobody can't find five minutes. You can do it before you get out of bed. You can do it in your car before you walk into work. You can do it sitting on the bathroom floor while your kids bang on the door.":
        "Documents are not circulated for convenience. If an assistant needs the schedule, they receive the schedule, not the supplier chain sitting behind it.",
    "It doesn't need to be pretty. It doesn't need to be Instagram-worthy. It just needs to happen.":
        "Names are matched to what immigration requires and nothing further. Where a reservation can lawfully be held under a company, it is.",
    "Sit somewhere comfortable. Set a timer for five minutes. Close your eyes or soften your gaze. Breathe normally. When your mind wanders (it will, immediately), notice it and come back to the feeling of your breath.":
        "Ask any provider one question: who, by name, will hold my full itinerary, and what exactly is each supplier told? A good answer is specific and slightly boring. A vague one tells you the promise is all there is.",
    "That's the whole thing. Do it tomorrow morning and see how you feel.":
        "Ask it before you need it, rather than after something has appeared somewhere it should not have.",
    "No app required. No special cushion. No incense. Just you and five minutes.":
        "No certificate required. No clause in a contract on its own. Just a process that limits what each person is told.",

    # ---- saying no -----------------------------------------------------------
    "This is probably the thing I talk about most in my practice. Not because I go looking for it, but because it comes up with almost every single client.":
        "This is the thing new clients ask about most, usually because no travel provider has ever told them no before.",
    "Most people know they need better boundaries. That's not the issue. The issue is that every time they try to set one, they feel like a terrible person.":
        "Most providers know when a schedule is not going to hold. That is not the issue. The issue is that saying so risks the booking, so they accept it and hope.",
    "They say no to staying late at work and immediately feel guilty. They tell a friend they can't make it to something and spend the rest of the evening worrying they've upset them. They ask their partner for some time alone and then feel selfish for wanting it.":
        "They accept a five-city week with no allowance for crew duty. They confirm a slot that has not yet been granted. They agree a ninety-minute connection through an airport where the transfer alone takes an hour.",
    "This guilt isn't a sign that you're doing something wrong. It's a sign that you've been trained to put everyone else's comfort above your own for so long that prioritising yourself feels foreign.":
        "The client hears yes and plans the rest of the week around it. The failure arrives later, on a day when there is nothing left to be done about it.",
    "Boundary problems almost always trace back to childhood. Not necessarily anything dramatic. Sometimes it's just growing up in a household where being \"good\" meant being agreeable, where saying no was seen as being difficult, where love felt conditional on being easy to be around.":
        "It comes from treating travel as a sale rather than as an operation. In a sale, no is a lost deal. In an operation, no is information, and it is worth far more during planning than at any point afterwards.",
    "You learn that your needs are less important than keeping the peace. And you carry that into adulthood without questioning it.":
        "Providers who never say no are not more capable. They have moved the problem to the day of travel, where it stops being theirs and becomes yours.",
    "A boundary isn't a wall. It's not about shutting people out or being cold. A boundary is just a clear statement about what you're okay with and what you're not.":
        "It is not a refusal. It is a constraint and an alternative, offered in the same sentence.",
    "\"I can't take calls after 7pm.\" \"I need the weekend to myself.\" \"I'm not comfortable discussing that.\"":
        "\"That connection is forty minutes short of what the transfer needs, so either the meeting moves to eleven or we take the earlier slot.\" \"The crew runs out of hours on the fourth leg, so the last sector flies in the morning or we position a second crew.\"",
    "These aren't aggressive statements. They're honest ones. And the right people in your life will respect them. The ones who don't are showing you exactly why the boundary was necessary in the first place.":
        "These are not obstructive answers. They are specific ones, and they arrive while there is still time to choose between them.",
    "Setting boundaries gets easier with practice, but the guilt doesn't disappear overnight. You have to be willing to sit with the discomfort for a while. It's uncomfortable in the same way any new habit is uncomfortable: not because it's wrong, but because it's unfamiliar.":
        "It is uncomfortable to tell a principal that what they have asked for cannot be done as written. It is considerably more uncomfortable to tell them at eleven at night in a terminal.",
    "What I tell my clients is this: the temporary discomfort of setting a boundary is always less than the long-term damage of never setting one. Every time you say yes when you mean no, you're borrowing from your future self. And at some point, the debt catches up.":
        "What we tell clients is this: the discomfort of a difficult conversation in the planning week is always smaller than the cost of the same conversation on the day. Every optimistic yes is borrowed from the journey itself.",
    "Start small. One boundary this week. Notice the guilt, let it be there, and don't act on it. That's the whole practice.":
        "So we say it early, with the alternative attached. That is the whole of it.",

    # ---- pre-departure checks ------------------------------------------------
    "People ask me about nutrition a lot, which makes sense given that it's one of the areas I work in. But what they usually want is a meal plan or a list of \"good\" and \"bad\" foods. I don't do that.":
        "People ask what we actually do in the day before a journey, and usually expect a long checklist. It is shorter than they imagine, because it was built from what has gone wrong rather than from everything that could.",
    "I counted calories and tracked macros for about two years. I was meticulous about it. And technically it worked: I hit my targets, I looked healthy on paper, I was eating \"clean\" by anyone's definition.":
        "It is possible to build a pre-departure check with sixty items on it. We tried. Everything was ticked and the same three failures kept happening, because a list that long stops being read and starts being completed.",
    "But I was also miserable. I thought about food constantly. I felt guilty when I went over my numbers. Social meals became stressful because I couldn't control what was being served. I'd mentally calculate every plate that was put in front of me.":
        "A long list also buries the important items among the trivial ones. Confirming that the aircraft exists matters. Confirming a catering preference does not matter in the same way, and putting them on the same line treats them as though it did.",
    "That's not a healthy relationship with food, even if the food itself is healthy.":
        "So the list is short, and everything on it earned its place by failing once.",
    "I eat based on how things make me feel. Not in a vague \"listen to your body\" way, but in a practical, learned-over-time way. I know that if I skip breakfast I'll be irritable by 11am. I know that too much sugar at lunch makes my afternoon foggy. I know that I sleep better when I eat dinner earlier rather than later.":
        "Everything is reconfirmed with the person who will actually do it, not with the company that sold it. The driver, not the dispatcher. The handler, not the broker. A confirmation from somebody who will not be present on the day is not a confirmation.",
    "This isn't intuitive. I didn't wake up one day knowing all of this. I paid attention, experimented, and built a picture of what works for me over months. That's what I help my clients do too.":
        "This is not distrust. It is that information degrades as it passes along a chain, and the last person in the chain is the one the client actually meets.",
    "Breakfast is usually scrambled eggs with spinach and sourdough, or overnight oats with berries and seeds. Something with protein and fibre that keeps me going until lunch without thinking about food.":
        "In the morning, the aircraft and the crew. Tail number, slot times, crew duty against the full day, and whether anything on the route has changed since the permits were filed.",
    "Lunch varies but it's usually a big bowl of something: grains, vegetables, some kind of protein. I batch cook a lot of this on Sundays so I'm not making decisions at noon on a Tuesday.":
        "Around midday, the ground. Each driver contacted directly, each pickup point and terminal gate confirmed by name, and any closures or events checked in the cities involved.",
    "Afternoon I'll have a snack. Usually an apple with almond butter or a handful of nuts. Sometimes just a cup of tea and nothing else if I'm not hungry.":
        "In the afternoon, the arrivals. Handling agents at each airport, fast-track arranged and confirmed, and every name on the manifest matched exactly to the travel document.",
    "Dinner is whatever I feel like, honestly. Pasta, stir-fry, soup, fish and vegetables. I don't restrict anything. If I want pizza, I eat pizza. What I've noticed is that when you stop labelling foods as \"bad,\" you naturally gravitate toward balance because you're not rebounding from restriction.":
        "In the evening, the accommodation. Rooms confirmed as held rather than merely booked, arrival times passed on, and a fallback property identified in each city. Most of the time the fallback is never used, which is precisely why it costs so little to hold.",
    "Nutrition doesn't need to be complicated and it definitely doesn't need to be punishing. The best approach is the one you can maintain without thinking about it constantly. For me, that meant letting go of the spreadsheet and learning to actually listen.":
        "Pre-departure checks do not need to be elaborate and they certainly do not need to be theatrical. The best list is the one that gets read properly every time, which in practice means the one short enough to be.",
})

# --- journal subheadings and titles ------------------------------------------
NODE.update({
    "What I actually eat in a day": "What we check the day before departure",
    "Tired is temporary": "A booking is a single transaction",
    "Burnout is different": "An itinerary is a plan with slack in it",
    "Why this matters": "Why it matters",
    "The signals people miss": "Where the hours actually go",
    "What to do about it": "What we do about it",
    "Rest is not just sleep": "The aircraft is one of seven",
    "The seven types": "The seven",
    "Why this changes everything": "Why this changes the conversation",
    "The performance problem": "The promise problem",
    "What meditation actually is": "What discretion actually is",
    "Why five minutes is enough": "How it is enforced",
    "How to start": "What to ask",
    "The guilt problem": "The yes problem",
    "Where it comes from": "Where it comes from",
    "What a boundary actually is": "What saying no looks like",
    "The part nobody talks about": "The part nobody enjoys",
    "Why I stopped counting": "Why the list is short",
    "What I do instead": "Who we confirm with",
    "A typical day": "The day before",
    "The point": "The point",
})

# --- legal pages -------------------------------------------------------------
# The template ships a coach's policy with [Your Name] placeholders. This keeps
# its structure and swaps the service it describes; it still needs a real
# review before launch.

NODE.update({
    "Privacy Policy - Holistic": "Privacy Policy - Global Bridge",
    "Terms of Service - Holistic": "Terms of Service - Global Bridge",

    # Privacy policy
    "What I collect": "What we collect",
    "When you book a session": "When you request a call",
    "During coaching sessions": "While arranging travel",
    "How I use your information": "How we use your information",
    "I use the information I collect to:": "We use the information we collect to:",
    "Deliver coaching services and track your progress": "Arrange and manage your travel",
    "for scheduling sessions": "for scheduling calls",
    "Coaching session notes: Duration of our working relationship plus 12 months":
        "Travel records: Duration of our working relationship plus 12 months",
    "Access the personal information I hold about you":
        "Access the personal information we hold about you",

    # Terms of service
    "Coaching services": "Our services",
    "Discovery calls": "Introductory calls",
    "Paid sessions and programmes": "Travel arrangements",
    "Self-paced programmes:": "Deposits:",
    "Group programmes:": "Cancelled journeys:",
    "1:1 coaching packages:": "Retainers:",
})

TEXT.update({
    # Privacy policy
    "Your privacy matters to me. This policy explains what information I collect when you visit this website or use my coaching services, how I use it, and what rights you have over it.":
        "Your privacy matters to us. This policy explains what information we collect when you visit this website or ask us to arrange travel, how we use it, and what rights you have over it.",
    "This website is operated by [Your Name], trading as [Your Business Name].":
        "This website is operated by Global Bridge.",
    "If you have any questions about this policy, you can reach me at":
        "If you have any questions about this policy, you can reach us at",
    "I use basic analytics to understand how people find and use this site.":
        "We use basic analytics to understand how people find and use this site.",
    "If you book a discovery call or coaching session, I collect the information you provide through the booking form: your name, email address, and any details you share about what you're looking for.":
        "If you book an introductory call, we collect the information you provide through the booking form: your name, email address, and any details you share about the travel you need.",
    "I collect your name, email address, and the content of your message.":
        "We collect your name, email address, and the content of your message.",
    "I collect your email address and first name.":
        "We collect your email address and first name.",
    "I may take notes during our sessions to track your progress and inform future sessions. These notes are kept confidential and are not shared with anyone.":
        "We hold what is needed to arrange your journey, including travel document details, dates and preferences. Each supplier is given only what it needs for its own leg, and nothing further.",
    "Send you emails you've opted into (newsletters, session reminders)":
        "Send you emails you've opted into (newsletters, itinerary updates)",
    "I do not sell your personal information to third parties. I do not share your information with third parties for their marketing purposes.":
        "We do not sell your personal information. We do not share it with third parties for their marketing purposes.",
    "I keep your personal information only for as long as I need it. Specifically:":
        "We keep your personal information only for as long as we need it. Specifically:",
    "To exercise any of these rights, email me at":
        "To exercise any of these rights, email us at",
    "I will respond within 30 days.": "We will respond within 30 days.",
    "This website and my coaching services are not directed at children under the age of 16. I do not knowingly collect personal information from children.":
        "This website and our services are not directed at children under the age of 16. We do not knowingly collect personal information from children.",
    "I may update this policy from time to time. Any changes will be posted on this page with an updated revision date. If I make significant changes, I will let you know via email where possible.":
        "We may update this policy from time to time. Any changes will be posted on this page with an updated revision date. If we make significant changes, we will let you know by email where possible.",
    "If you have any questions about this privacy policy, contact me at":
        "If you have any questions about this privacy policy, contact us at",

    # Terms of service
    "By accessing this website or purchasing coaching services from [Your Name], trading as [Your Business Name], you agree to these terms. If you do not agree, please do not use this website or purchase services.":
        "By accessing this website or engaging Global Bridge to arrange travel, you agree to these terms. If you do not agree, please do not use this website or engage our services.",
    "The coaching services offered through this website are for educational and personal development purposes. I am a certified wellness coach, not a licensed therapist, psychologist, or medical professional.":
        "Global Bridge arranges travel and related services on your behalf. We act as an agent: aircraft, vehicles, accommodation and other services are provided by third-party operators, each under its own terms and conditions.",
    "Coaching is not a substitute for professional medical advice, diagnosis, or treatment. If you are experiencing a medical or mental health emergency, please contact your local emergency services or a licensed healthcare provider.":
        "We are not an air carrier and we do not operate aircraft or vehicles. Operators are selected for their licensing and safety record, and remain responsible for the services they provide.",
    "are billed as described on the Services page. Payment is due at the time of booking unless otherwise agreed.":
        "are quoted individually and confirmed in writing before anything is booked. Payment is due on confirmation unless otherwise agreed.",
    "I ask for at least 24 hours notice if you need to cancel or reschedule a session. Cancellations made with less than 24 hours notice may be charged in full.":
        "Cancellation terms follow those of the operators involved. Charter, accommodation and ground bookings often carry their own charges, which we state in writing before you confirm.",
    "If I need to cancel or reschedule a session, I will give you as much notice as possible and offer an alternative time.":
        "If an operator cancels, we arrange the nearest alternative available and tell you as soon as we know.",
    "Due to the digital nature of these products, refunds are not available once access has been granted.":
        "Amounts already committed to an operator on your behalf cannot be returned once that operator has charged them.",
    "A full refund is available if you withdraw within 7 days of purchase, provided the programme has not yet started. Once the programme has started, refunds are not available.":
        "Where an operator refunds us, we pass that refund on in full. Our own fee is returned if nothing has yet been booked on your behalf.",
    "A pro-rated refund may be available for unused sessions if you wish to discontinue coaching. This is assessed on a case-by-case basis.":
        "A retainer may be ended with thirty days' notice, and any unused portion is assessed case by case.",
    "Everything discussed during coaching sessions is confidential. I will not share your personal information or session content with anyone without your explicit consent, except where I am legally required to do so (for example, if there is a risk of harm to yourself or others).":
        "Your itinerary and travel details are confidential. Each supplier is told only what it needs for its own leg, and nothing further is shared without your consent, except where we are legally required to do so.",
    "All content on this website, including text, images, graphics, and design, is owned by [Your Name] and is protected by copyright law.":
        "All content on this website, including text, images, graphics and design, is owned by Global Bridge and protected by copyright law.",
    "Materials provided as part of coaching programmes (worksheets, guides, resources) are for your personal use only and may not be shared or redistributed.":
        "Itineraries and documents prepared for you are for your own use and may not be shared or redistributed.",
    "Coaching is a collaborative process and results vary depending on individual circumstances and effort. I do not guarantee specific outcomes from coaching services.":
        "Travel depends on air traffic control, weather, immigration and third-party operators. We cannot guarantee schedules that are outside our control.",
    "To the fullest extent permitted by law, I am not liable for any indirect, incidental, or consequential damages arising from your use of this website or coaching services.":
        "To the fullest extent permitted by law, we are not liable for any indirect, incidental or consequential loss arising from your use of this website or our services.",
    "I may update these terms from time to time. Continued use of the website or services after changes constitutes acceptance of the updated terms.":
        "We may update these terms from time to time. Continued use of the website or our services after changes constitutes acceptance of the updated terms.",
    "If you have any questions about these terms, contact me at":
        "If you have any questions about these terms, contact us at",
})

def plain_forms():
    """MARKUP and WORD_SPLIT as flat sentences.

    Framer's search index stores a heading as one string, without the spans the
    page splits it into, so the same headings need a markup-free form.
    """
    pairs = dict(WORD_SPLIT)
    for pattern, repl in MARKUP:
        old = (pattern.replace("(<span[^>]*>)", "").replace("</span>", "")
               .lstrip(">").replace("\\.", "."))
        new = repl.replace("\\1", "").replace("</span>", "").lstrip(">")
        pairs[old] = new
    return pairs

def accent_parts():
    """MARKUP split into the text runs either side of the coloured word.

    The page modules build the same heading as a JavaScript array of runs
    rather than as markup, so each run has to be matched on its own.
    """
    out = []
    for pattern, repl in MARKUP:
        old = re.split(r"\(<span\[\^>\]\*>\)|</span>", pattern)
        new = re.split(r"\\1|</span>", repl)
        clean = lambda xs: [x.lstrip(">").replace("\\.", ".") for x in xs if x != ""]
        out.append((clean(old), clean(new)))
    return out

def json_forms(s: str):
    """The same string as written in the page, in Framer's hydration payload
    (JSON, quotes escaped once) and in richtext inside it (escaped twice)."""
    return (s, s.replace('"', r'\"'), s.replace('"', r'\\\"'))


SPAN_RE = re.compile(
    r'<span style="display:inline-block;opacity:0\.001;[^"]*">([^<]*)</span>'
    r'(\s*)', re.S)


def rebuild_word_spans(html: str, seen: set) -> tuple[str, int]:
    """Replace runs of per-word animated spans whose text matches a heading.

    Framer interleaves empty animated spans between the words, so matching
    ignores them; the rebuilt run replaces everything from the first word span
    to the last, empties included.
    """
    count = 0
    for old, new in WORD_SPLIT.items():
        old_words = old.split(" ")
        while True:
            spans = list(SPAN_RE.finditer(html))
            words = [(i, m) for i, m in enumerate(spans) if m.group(1).strip()]
            hit = None
            for i in range(len(words) - len(old_words) + 1):
                run = words[i:i + len(old_words)]
                if [m.group(1) for _, m in run] == old_words:
                    hit = [m for _, m in run]
                    break
            if hit is None:
                break
            style = re.search(r'style="([^"]*)"', hit[0].group(0)).group(1)
            rebuilt = " ".join(
                f'<span style="{style}">{w}</span>' for w in new.split(" "))
            html = html[:hit[0].start()] + rebuilt + html[hit[-1].end():]
            seen.add(old)
            count += 1
    return html, count


def main() -> None:
    short = [k for k in TEXT if len(k) < MIN_TEXT_KEY]
    if short:
        sys.exit("TEXT keys too short to be unambiguous, move them to NODE: "
                 + ", ".join(repr(k) for k in short))

    root = pathlib.Path(__file__).resolve().parent.parent
    files = sorted(p for p in root.rglob("*.html") if ".git" not in p.parts)
    counts = {"heading": 0, "markup": 0, "node": 0, "text": 0, "slug": 0}
    seen = set()

    for path in files:
        html = path.read_text(encoding="utf-8")
        before = html

        html, heads = rebuild_word_spans(html, seen)
        counts["heading"] += heads

        for pattern, repl in MARKUP:
            html, n = re.subn(pattern, repl, html)
            counts["markup"] += n
            if n:
                seen.add(pattern)

        for old, new in NODE.items():
            # ">text<" is the rendered node; the quoted forms are the same node
            # inside Framer's hydration JSON, which React would otherwise
            # restore over the rendered page.
            # an attribute value escapes its own quotes as &quot;
            ao, an = (x.replace('"', "&quot;") for x in (old, new))
            pairs = [(f">{old}<", f">{new}<"),
                     (f'="{old}"', f'="{new}"'),
                     (f'="{ao}"', f'="{an}"')]
            pairs += [(f'{q}{o}{q}', f'{q}{n}{q}') for q, o, n
                      in zip((r'\"', r'\\\"'), json_forms(old)[1:],
                             json_forms(new)[1:])]
            for key, repl in pairs:
                if key in html:
                    counts["node"] += html.count(key)
                    seen.add(old)
                    html = html.replace(key, repl)

        for old, new in TEXT.items():
            for o, n in zip(json_forms(old), json_forms(new)):
                if o in html:
                    counts["text"] += html.count(o)
                    seen.add(old)
                    html = html.replace(o, n)

        for old, new in SLUGS.items():
            if old in html:
                counts["slug"] += html.count(old)
                seen.add(old)
                html = html.replace(old, new)

        if html != before:
            path.write_text(html, encoding="utf-8")
            print(f"  {path.relative_to(root)}")

    for old, new in SLUGS.items():
        src = root / "journal" / old
        if src.is_dir():
            src.rename(root / "journal" / new)

    print("rewrote {heading} split headings, {markup} accent headings, "
          "{node} labels, {text} strings and {slug} links".format(**counts)
          + f" across {len(files)} pages")

    missed = [k for k in
              list(WORD_SPLIT) + [p for p, _ in MARKUP] + list(NODE)
              + list(TEXT) + list(SLUGS)
              if k not in seen]
    if missed:
        print(f"\n{len(missed)} keys matched nothing:")
        for k in missed:
            print(f"  {k!r}")


if __name__ == "__main__":
    main()
