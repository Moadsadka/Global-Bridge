import type { Metadata } from "next";
import { DM_Sans } from "next/font/google";
import { MotionProvider } from "@/components/MotionProvider";
import "./globals.css";

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Global Bridge — VIP Business & Travel Services",
  description:
    "Private aviation, executive transfers and business concierge for principals travelling between Europe, North Africa and the Gulf. Arranged with absolute discretion.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${dmSans.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-paper text-stone">
        <MotionProvider>{children}</MotionProvider>
      </body>
    </html>
  );
}
