import NextLink from "next/link";
import {
  AnchorHTMLAttributes,
  DetailedHTMLProps,
  ReactElement,
  ReactNode,
} from "react";
import { UrlObject } from "url";

type LinkProps = {
  href: string | UrlObject;
  children: ReactNode;
} & DetailedHTMLProps<
  AnchorHTMLAttributes<HTMLAnchorElement>,
  HTMLAnchorElement
>;

export function Link({ href, children, ...props }: LinkProps): ReactElement {
  return (
    <NextLink href={href} passHref>
      <a href="#top" {...props}>
        {children}
      </a>
    </NextLink>
  );
}
