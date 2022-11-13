import { FunctionComponent, ReactNode } from "react";
import Image from 'next/image';
import Link from 'next/link';

interface IProps {
    main: ReactNode
};

const Layout: FunctionComponent<IProps> = ({ main }) => {
    return (
        <div className=" max-w-screen-2xl px-5 mx-auto text-blue">
            <nav className="rounded-lg bg-green my-5" style={{ height: "64px " }}>
                <div className="px-6 flex items-center justify-between h-16">
                    <Link href='/'>
                        <Image
                            src='/img/logo@2x.png'
                            width={150}
                            height={50}
                        />
                    </Link>
                    <button className="text-white">
                        Hello
                    </button>
                </div>
            </nav>
            <main>
                {main}
            </main>
        </div >
    );
};

export default Layout;