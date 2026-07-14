import { Phone, MapPin, Globe } from 'lucide-react'
import logo from '@/assets/logo.png'
import Image from 'next/image'

export const Footer = () => {
  return (
    <footer id="contact" className="bg-footer text-footer-foreground py-16">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-12">
          {/* Logo & Description */}
          <div>
            <Image
              src={logo}
              alt="Nomos Logo"
              className="h-12 mb-6 brightness-0 invert"
            />
            <p className="text-footer-foreground/70 mb-6 leading-relaxed">
              Prototyp systemu Nomos służy wyłącznie celom badawczym i rozwojowym..
            </p>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-bold mb-6">Kontakt</h3>
            <ul className="space-y-4">
              <li className="flex items-center gap-3">
                <Phone size={18} className="text-primary" />
                <a
                  href="tel:+48602508641"
                  className="text-footer-foreground/70 hover:text-footer-foreground transition-colors"
                >
                  +48 602 508 641
                </a>
              </li>
              <li className="flex items-center gap-3">
                <Globe size={18} className="text-primary" />
                <a
                  href="https://galicea.pl"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-footer-foreground/70 hover:text-footer-foreground transition-colors"
                >
                  galicea.pl
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-lg font-bold mb-6">Informacje o projekcie</h3>
            <div className="text-background/70 text-sm leading-relaxed">
              <p className="mb-4">
                <a
                  href="https://github.com/galicea/nomos"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-footer-foreground/70 hover:text-footer-foreground transition-colors"
                >
                  https://github.com/galicea/nomos
                </a>
              </p>
              <p className="mb-4">
                wersja 0.0.1 - tylko do celów testowych
              </p>
            </div>
          </div>
        </div>

        <div className="border-t border-background/10 mt-12 pt-8 text-center text-background/50 text-sm">
          <p>
            © {new Date().getFullYear()}  GNU GENERAL PUBLIC LICENSE.
          </p>
        </div>
      </div>
    </footer>
  )
}
