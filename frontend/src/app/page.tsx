"use client";

import { useState } from "react";
import { Search, MapPin, Sparkles, MessageSquare } from "lucide-react";
import { searchSpots } from "@/lib/api";
import { SearchResponse } from "@/types";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function VibeSearchPage() {
  const [input, setInput] = useState("");
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<SearchResponse | null>(null);

  const handleSearch = async (e?: React.FormEvent, directInput?: string) => {
    if (e) e.preventDefault();
    
    const searchInput = directInput || [input, ...selectedKeywords].filter(Boolean).join(" ");
    if (!searchInput.trim()) return;

    setIsLoading(true);
    try {
      const data = await searchSpots(searchInput);
      setResults(data);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const RECOMMEND_KEYWORDS = [
    "作業", "デート", "集中", "ケーキ", "読書", "夜景", "電源あり", "Wi-Fi完備", 
    "静か", "おしゃれ", "隠れ家", "朝活", "テラス席", "レトロ", "和風", "一人で", 
    "癒やし", "絶景", "モーニング", "深夜営業"
  ];

  const AREAS = ["渋谷", "新宿", "銀座", "表参道", "六本木", "自由が丘", "鎌倉"];

  const handleKeywordToggle = (keyword: string) => {
    setSelectedKeywords((prev) => {
      const isSelected = prev.includes(keyword);
      if (isSelected) {
        return prev.filter((k) => k !== keyword);
      } else {
        return [...prev, keyword];
      }
    });
  };

  const handleAreaClick = (area: string) => {
    setInput(area);
  };

  return (
    <main className="min-h-screen bg-[#fdfcfb] text-slate-600 font-sans selection:bg-[#fdf2f0] selection:text-[#f19066]">
      <div className="max-w-5xl mx-auto px-6 py-16 md:py-24">
        
        {/* 1. Header Area - Soft Apricot Tone */}
        <div className="text-center mb-24 space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#fdf2f0] border border-[#fbd3c1] text-[#f19066] text-xs font-bold tracking-widest uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Finding your vibe</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-slate-800">
            Vibe<span className="text-[#f19066]">Search</span>
          </h1>
          <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto font-medium leading-relaxed">
            心地よい「雰囲気」を、AIがそっと見つけ出します。<br className="hidden md:block" />
            あなたの感性に寄り添う、場所探しのお手伝い。
          </p>
        </div>

        {/* 2. Search Area - Organic & Muted */}
        <div className="relative z-50 mb-32 space-y-12">
          
          {/* Area Selector */}
          <div className="space-y-4">
            <div className="flex items-center justify-center gap-3 text-slate-200">
              <div className="h-[1px] w-12 bg-slate-100" />
              <span className="text-[10px] font-black uppercase tracking-[0.3em]">Explore Areas</span>
              <div className="h-[1px] w-12 bg-slate-100" />
            </div>
            <div className="flex flex-wrap justify-center gap-3">
              {AREAS.map((area) => (
                <button
                  key={area}
                  onClick={() => handleAreaClick(area)}
                  className={cn(
                    "px-5 py-2 rounded-xl text-sm font-bold transition-all duration-300 border",
                    input.includes(area)
                      ? "bg-[#64748b] border-[#64748b] text-white shadow-md scale-105"
                      : "bg-white border-slate-100 text-slate-400 hover:bg-slate-50 hover:text-slate-600 hover:border-slate-200"
                  )}
                >
                  {area}
                </button>
              ))}
            </div>
          </div>

          {/* Main Search Bar - Clean & Softly Floating */}
          <form onSubmit={(e) => handleSearch(e)} className="max-w-2xl mx-auto">
            <div className="relative group">
              <div className="relative flex items-center bg-white border border-slate-100 rounded-3xl shadow-xl shadow-slate-200/30 group-focus-within:border-[#fbd3c1] transition-all duration-500 overflow-hidden">
                <div className="pl-8 text-slate-200">
                  <Search className="w-6 h-6" />
                </div>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="どんな雰囲気の場所をお探しですか？"
                  readOnly={isLoading}
                  className="w-full h-20 px-6 bg-transparent outline-none text-xl text-slate-600 placeholder:text-slate-200 font-medium"
                />
                <div className="pr-4">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className={cn(
                      "h-12 px-8 rounded-2xl font-bold text-sm transition-all duration-300",
                      isLoading 
                        ? "bg-slate-50 text-slate-300 cursor-wait" 
                        : "bg-[#f19066] text-white hover:bg-[#cf7a52] active:scale-95 shadow-lg shadow-[#f19066]/20"
                    )}
                  >
                    {isLoading ? "Analyzing..." : "Find Vibes"}
                  </button>
                </div>
              </div>
            </div>
          </form>

          {/* Vibe Chips - Muted Apricot */}
          <div className="space-y-6">
            <div className="flex items-center justify-center gap-3 text-slate-200">
              <div className="h-[1px] w-12 bg-slate-100" />
              <span className="text-[10px] font-black uppercase tracking-[0.3em]">Personalize Vibes</span>
              <div className="h-[1px] w-12 bg-slate-100" />
            </div>
            <div className="flex flex-wrap justify-center gap-2 max-w-3xl mx-auto">
              {RECOMMEND_KEYWORDS.map((keyword) => {
                const isSelected = selectedKeywords.includes(keyword);
                return (
                  <button
                    key={keyword}
                    onClick={() => handleKeywordToggle(keyword)}
                    className={cn(
                      "px-4 py-2 rounded-full text-xs font-bold transition-all duration-300 border",
                      isSelected 
                        ? "bg-[#fdf2f0] border-[#fbd3c1] text-[#f19066] shadow-sm" 
                        : "bg-white border-slate-100 text-slate-400 hover:border-slate-200 hover:text-slate-500"
                    )}
                  >
                    {keyword}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* 3. Results Area */}
        {results && (
          <div className="space-y-20 animate-in">
            
            {/* AI Insight Header */}
            <div className="bg-white/60 backdrop-blur-md border border-slate-100 p-10 rounded-[2.5rem] shadow-sm text-center">
              <div className="flex flex-col items-center gap-4">
                <div className="p-3 bg-[#fdf2f0] rounded-2xl text-[#f19066]">
                  <Sparkles className="w-6 h-6" />
                </div>
                <h2 className="text-xl font-bold text-slate-800 tracking-tight">あなたの「こだわり」を整理しました</h2>
                <div className="flex flex-wrap justify-center gap-3 mt-2">
                  <span className="inline-flex items-center gap-2 px-4 py-2 bg-slate-50 text-slate-500 rounded-xl text-xs font-bold border border-slate-100">
                    📍 {results.intent.location || "どこでも"}
                  </span>
                  {results.intent.vibe.map((v, i) => (
                    <span key={i} className="inline-flex items-center px-4 py-2 bg-[#fdf2f0] text-[#f19066] rounded-xl text-xs font-bold border border-[#fbd3c1]/50">
                      #{v}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Spot List */}
            <div className="grid grid-cols-1 gap-12">
              {results.recommendations.map((spot) => (
                <div
                  key={spot.id}
                  className="group relative bg-white border border-slate-100 rounded-[2rem] overflow-hidden shadow-sm hover:shadow-xl hover:shadow-slate-200/20 transition-all duration-700 flex flex-col md:flex-row"
                >
                  <div className="absolute top-6 left-6 z-20">
                    {spot.status && (
                      <div className={cn(
                        "px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider backdrop-blur-xl border shadow-sm",
                        spot.status === "営業中" ? "bg-white/80 border-green-100 text-green-500" :
                        spot.status === "まもなく終了" ? "bg-white/80 border-orange-100 text-[#f19066]" :
                        "bg-white/80 border-slate-50 text-slate-300"
                      )}>
                        {spot.status}
                      </div>
                    )}
                  </div>

                  {spot.image_url && (
                    <div className="relative w-full md:w-80 h-64 md:h-auto overflow-hidden shrink-0">
                      <img 
                        src={spot.image_url} 
                        alt={spot.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-1000"
                      />
                      <div className="absolute inset-0 bg-gradient-to-r from-white/10 to-transparent" />
                    </div>
                  )}

                  <div className="p-10 md:p-12 flex flex-col flex-1">
                    <div className="flex flex-col md:flex-row justify-between items-start gap-6 mb-8">
                      <div className="space-y-2">
                        <h3 className="text-3xl font-bold text-slate-800 tracking-tight leading-tight group-hover:text-[#f19066] transition-colors">
                          {spot.name}
                        </h3>
                        <div className="flex items-center gap-2 text-slate-400 font-medium text-sm">
                          <MapPin className="w-4 h-4 text-slate-300" />
                          {spot.address}
                        </div>
                      </div>
                      <a 
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(spot.name + " " + spot.address)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="p-3 bg-slate-50 hover:bg-slate-100 text-slate-400 rounded-2xl transition-all border border-slate-100"
                      >
                        <MapPin className="w-5 h-5" />
                      </a>
                    </div>
                    
                    {spot.vibe_summary && (
                      <div className="relative mb-10">
                        <p className="text-slate-500 text-lg font-medium leading-relaxed">
                          {spot.vibe_summary}
                        </p>
                      </div>
                    )}
                    
                    <div className="mt-auto flex items-center justify-between pt-8 border-t border-slate-50">
                      <div className="flex items-center gap-4">
                        <div className="px-4 py-1.5 bg-slate-50 text-slate-400 rounded-lg text-[10px] font-black uppercase tracking-[0.2em]">
                          {spot.metadata.price_range || "Budget info n/a"}
                        </div>
                        {spot.crowd && (
                          <span className={cn(
                            "px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest border",
                            spot.crowd === "空いています" ? "bg-blue-50 border-blue-100 text-blue-600" :
                            spot.crowd === "混雑しています" ? "bg-orange-50 border-orange-100 text-orange-600" :
                            "bg-slate-50 border-slate-100 text-slate-400"
                          )}>
                            {spot.crowd}
                          </span>
                        )}
                      </div>
                      <a 
                        href={`https://www.google.com/search?q=${encodeURIComponent(spot.name)}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="group/btn inline-flex items-center gap-2 text-[#f19066] font-bold text-sm"
                      >
                        Discover more
                        <span className="group-hover:translate-x-1 transition-transform">→</span>
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* No Results Fallback */}
            {results.recommendations.length === 0 && (
              <div className="text-center py-24 border-2 border-dashed border-slate-200 rounded-[2rem]">
                <div className="text-slate-300 mb-4 flex justify-center">
                  <Search className="w-12 h-12" />
                </div>
                <p className="text-slate-500 font-medium">条件に合うスポットが見つかりませんでした。</p>
                <button onClick={() => setResults(null)} className="mt-4 text-[#f19066] font-bold text-sm hover:underline">
                  検索条件をクリアする
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
