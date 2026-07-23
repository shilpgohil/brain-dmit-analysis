import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { ArrowLeft } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center p-6">
      <p className="text-[80px] font-bold text-slate-800 leading-none mb-4">404</p>
      <h1 className="text-lg font-semibold text-slate-300 mb-2">Page not found</h1>
      <p className="text-sm text-slate-600 mb-6">
        The page you are looking for does not exist.
      </p>
      <Link href="/">
        <Button icon={<ArrowLeft className="w-4 h-4" />}>Back to Overview</Button>
      </Link>
    </div>
  );
}
