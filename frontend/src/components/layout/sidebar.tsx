"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/jobs", label: "Jobs" },
  { href: "/approvals", label: "Approvals" },
  { href: "/scheduled-tasks", label: "Scheduled Tasks" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 border-r border-slate-200 bg-white md:flex md:flex-col">
      <div className="border-b border-slate-200 px-6 py-5">
        <h2 className="text-xl font-semibold">ETAP</h2>
        <p className="mt-1 text-sm text-slate-500">Automation Platform</p>
      </div>

      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {links.map((link) => {
            const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);

            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={`block rounded-xl px-4 py-2 text-sm font-medium transition ${
                    isActive
                      ? "bg-slate-900 text-white"
                      : "text-slate-700 hover:bg-slate-100"
                  }`}
                >
                  {link.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}