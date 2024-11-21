import Link from "next/link";

export default function Home() {
  return (
    <ul>
      <li>
        <Link href="/uno" className="underline text-blue-600">
          UNO
        </Link>
      </li>
    </ul>
  );
}
