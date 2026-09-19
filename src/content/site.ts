/**
 * Site copy.
 *
 * Written from the company's own letterhead and business cards, which describe
 * the services and carry the real contact details. Anything marked TODO is a
 * placeholder that needs a real figure from the client before launch.
 */

export const company = {
  name: "Global Bridge",
  tagline: "Corporate Solutions & Business Services",
  email: "vip@gbinvestor.com",
  site: "www.gbinvestor.com",
  offices: [
    {
      city: "Valencia",
      country: "Spain",
      lines: [
        "Avenida de las Cortes Valencianas 58",
        "Torre Empresarial Valencia, Floor 12, Office 1204",
        "46015 Valencia, Spain",
      ],
      tel: "+34 960 845 730",
      mobile: "+34 611 284 915",
    },
    {
      city: "Tripoli",
      country: "Libya",
      lines: ["Al-Andalus District, Gargaresh Road", "Tripoli, Libya"],
      tel: "+218 21 477 2840",
    },
  ],
};

export const hero = {
  eyebrow: "Valencia · Tripoli",
  headlineBefore: "Every",
  rotating: ["journey", "transfer", "arrival", "engagement"],
  headlineAfter: "handled — from departure to return",
  supporting:
    "Private aviation, executive ground transport and business concierge for principals moving between Europe, North Africa and the Gulf. Arranged end to end, with absolute discretion.",
  cta: "Request arrangements",
  ctaSecondary: "Speak to our team",
  placeholder: "Email address",
};

export const heroStats = [
  // TODO: replace with the client's real figures before launch.
  { value: "2", label: "offices, Valencia and Tripoli" },
  { value: "24/7", label: "coordination desk" },
];

export const services = [
  {
    title: "Private aviation",
    body: "Private jet charter, VIP terminal access and flight coordination, arranged around your schedule rather than a timetable.",
    tags: ["Charter", "VIP terminal", "Flight coordination"],
    tone: "espresso",
  },
  {
    title: "Executive ground transport",
    body: "Chauffeured luxury vehicles for every leg — hotel to terminal, terminal to meeting, and every transfer in between.",
    tags: ["Chauffeur", "Airport transfer", "Close protection"],
    tone: "copper",
  },
  {
    title: "VIP airport services",
    body: "Fast-track immigration, baggage assistance and discreet departure procedures at both ends of the journey.",
    tags: ["Fast-track", "Baggage", "Departure"],
    tone: "cream",
  },
  {
    title: "Business concierge",
    body: "Accommodation at leading hotels and resorts, meeting coordination and executive assistance throughout your engagements.",
    tags: ["Accommodation", "Meetings", "Concierge"],
    tone: "gold",
  },
];

export const friction = {
  heading: "The arrangements that slow a principal down",
  items: [
    { lead: "No more", rest: "commercial terminals and public queues" },
    { lead: "Forget", rest: "chasing three suppliers for one itinerary" },
    { lead: "Stop", rest: "briefing a new driver in every city" },
    { lead: "Skip", rest: "hotels that cannot hold a room at short notice" },
    { lead: "Done with", rest: "itineraries that leak beyond your office" },
    { lead: "Never again", rest: "a transfer that misses the aircraft" },
  ],
};

export const stats = [
  // TODO: replace with the client's real figures before launch.
  { value: "100%", label: "of itineraries managed end to end" },
  { value: "3", label: "regions covered — Europe, North Africa, the Gulf" },
  { value: "24/7", label: "direct line to your coordinator" },
];

export const testimonials = [
  // TODO: replace with real, attributed client quotes before launch.
  {
    quote:
      "Four cities in six days and not one arrangement needed my attention. The transfers were waiting before we landed.",
    name: "Managing Director",
    role: "Private investment office",
  },
  {
    quote:
      "They understand that discretion is the service. Nothing about our travel left their desk.",
    name: "Chief Executive",
    role: "Industrial group",
  },
];

export const finalCta = {
  heading: "One call and the itinerary is handled",
  body: "Tell us where you need to be. We arrange the rest — aircraft, transfers, accommodation and everything between.",
  cta: "Request arrangements",
};

export const nav = [
  { label: "Services", href: "#services" },
  { label: "How we work", href: "#how" },
  { label: "Coverage", href: "#coverage" },
  { label: "Contact", href: "#contact" },
];
