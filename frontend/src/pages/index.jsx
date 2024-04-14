"use client";

import Link from 'next/link';

export default function Home({ posts }) {
  return (
    <main>
      <div className="hero min-h-screen bg-base-200">
      <div className="hero-content text-center">
      <div className="max-w-md">
      <h1 className="text-5xl font-bold">Welcome to IKOI</h1>
      <p className="py-10 text1-2xl">"Peace begins with a smile." -Mother Teresa</p>
      
      <Link href="/app/others/login" passHref>
      <button className="btn btn-active btn-primary text-lg mr-7">Get Started</button>
      </Link>
      
    </div>
  </div>
</div>
    </main>
  );
}
