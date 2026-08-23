"use client";

import Image from "next/image";
import { motion } from "framer-motion";

/** Official brand mark — gold-ringed fingerprint/neural medallion logo. */
export function NavBrandMark() {
  return (
    <motion.div
      className="relative w-9 h-9 rounded-full overflow-hidden flex-shrink-0"
      style={{
        boxShadow: "0 0 16px rgba(196,165,116,0.25)",
      }}
      whileHover={{ scale: 1.08 }}
      transition={{ type: "spring", stiffness: 400, damping: 22 }}
    >
      <Image
        src="/images/logo.png"
        alt="DMIT logo"
        fill
        sizes="36px"
        className="object-contain"
        priority
      />
    </motion.div>
  );
}
