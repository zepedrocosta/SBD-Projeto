% report.cls

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Template for report in LaTeX for FCT NOVA
% Main class file
%
% Author: José Costa (https://github.com/zepedrocosta)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}

% Load the article class with some default options
\LoadClass[a4paper,10pt]{article}

% Required packages
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{helvet}
\RequirePackage{hyperref}
\RequirePackage{tocloft} % For customizing the table of contents
% \RequirePackage[portuguese]{babel} % Set language to Portuguese
\RequirePackage[utf8]{inputenc} % For UTF-8 encoding
\RequirePackage{lipsum} % For dummy text
\RequirePackage[backend=biber]{biblatex}
\RequirePackage{csquotes}
\RequirePackage{setspace}
\RequirePackage{xcolor}
\RequirePackage{listings}

\definecolor{clr-background}{RGB}{255,255,255}
\definecolor{clr-text}{RGB}{0,0,0}
\definecolor{clr-string}{RGB}{163,21,21}
\definecolor{clr-namespace}{RGB}{0,0,0}
\definecolor{clr-preprocessor}{RGB}{128,128,128}
\definecolor{clr-keyword}{RGB}{0,0,255}
\definecolor{clr-type}{RGB}{43,145,175}
\definecolor{clr-variable}{RGB}{0,0,0}
\definecolor{clr-constant}{RGB}{111,0,138} % macro color
\definecolor{clr-comment}{RGB}{0,128,0}

\lstset{
    backgroundcolor=\color{clr-background},
	  basicstyle=\color{clr-text}, % any text
	  stringstyle=\color{clr-string},
	  identifierstyle=\color{clr-variable}, 
	  commentstyle=\color{clr-comment},
	  keywordstyle=\color{clr-type},
	  keywordstyle={[2]\color{clr-constant}},
    captionpos=t,
    basicstyle={\ttfamily\footnotesize},
    numbers=left,
    numberstyle={\ttfamily\tiny},
    tabsize=2,
    float,
    frame=single,
    columns=fullflexible,
    breaklines=true,
    postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
    inputencoding=utf8,
    extendedchars=true,
    showspaces=false,  % Ensure spaces are not visually marked
    showstringspaces=false, % Prevent spaces in strings from being marked
    literate=
      {á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
      {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
      {à}{{\`a}}1 {è}{{\`e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1
      {À}{{\`A}}1 {È}{{\'E}}1 {Ì}{{\`I}}1 {Ò}{{\`O}}1 {Ù}{{\`U}}1
      {ä}{{\"a}}1 {ë}{{\"e}}1 {ï}{{\"i}}1 {ö}{{\"o}}1 {ü}{{\"u}}1
      {Ä}{{\"A}}1 {Ë}{{\"E}}1 {Ï}{{\"I}}1 {Ö}{{\"O}}1 {Ü}{{\"U}}1
      {â}{{\^a}}1 {ê}{{\^e}}1 {î}{{\^i}}1 {ô}{{\^o}}1 {û}{{\^u}}1
      {Â}{{\^A}}1 {Ê}{{\^E}}1 {Î}{{\^I}}1 {Ô}{{\^O}}1 {Û}{{\^U}}1
      {œ}{{\oe}}1 {Œ}{{\OE}}1 {æ}{{\ae}}1 {Æ}{{\AE}}1 {ß}{{\ss}}1
      {ç}{{\c c}}1 {Ç}{{\c C}}1 {ø}{{\o}}1 {å}{{\r a}}1 {Å}{{\r A}}1
      {€}{{\EUR}}1 {£}{{\pounds}}1
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Custom area
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set the variables for the title page
\newcommand{\university}{NOVA University of Lisbon}
\newcommand{\faculty}{NOVA School of Science and Technology}
\newcommand{\course}{MSC in Computer Science}
% \newcommand{\project}{How do common open-source DBMSs perform under TPROC-C with fixed workloads}
\newcommand{\project}{Performance comparison between DBMSs under TPROC-C workloads}
\newcommand{\authorname}{José Costa (62637) \\ Rodrigo Albuquerque (70294) \\ Rodrigo Silva (70567)}
\newcommand{\subject}{Databases Systems}
\newcommand{\dateofsubmission}{\today} % Use \today for the current date

% Set the bibliography file
\addbibresource{bibliography.bib}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set default font to sans-serif
\renewcommand{\familydefault}{\sfdefault}

% Set page geometry
\geometry{a4paper, margin=1in}

% Custom table of contents
\setcounter{tocdepth}{4}

% Set the path for images
\graphicspath{{Images/}}

% Color for hyperlinks
\definecolor{darkblue}{rgb}{0.0,0.08,0.45}%
\hypersetup{
    colorlinks=true,
    linkcolor=darkblue,    % Color for internal links (e.g., TOC, \ref)
    citecolor=darkblue,    % Color for citation links
    urlcolor=darkblue      % Color for URL links
}
\PassOptionsToPackage{allcolors=darkblue}{hyperref}

% Custom title page
\newcommand{\maketitlepage}{
    \begin{titlepage}
        \centering

        \includegraphics[width=0.5\textwidth]{logo_nova_fct_en_v}\par

        \vspace{1cm}

        {\scshape\LARGE \university \par}

        \vspace{1cm}

        {\scshape\Large \course \par}

        \vspace{3cm}

        {\scshape\huge\bfseries \project \par}

        \vspace{2cm}

        {\Large\itshape \authorname \par}

        \vspace{3cm}

        {\scshape\large \subject \par}

        \vfill

        {\scshape\large \dateofsubmission \par}

        \doublespacing
        \tableofcontents
        \singlespacing

        \newpage
    \end{titlepage}
}

% Custom table of contents
\renewcommand{\cfttoctitlefont}{\huge\bfseries}
\renewcommand{\cftsecfont}{\large\bfseries}
\renewcommand{\cftsubsecfont}{\normalsize\bfseries}

% Custom section headings
\renewcommand{\section}{\@startsection{section}{1}{\z@}%
    {-3.5ex \@plus -1ex \@minus -.2ex}%
    {2.3ex \@plus.2ex}%
    {\normalfont\Large\bfseries}}

\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
    {-3.25ex \@plus -1ex \@minus -.2ex}%
    {1.5ex \@plus.2ex}%
    {\normalfont\large\bfseries}}

\endinput