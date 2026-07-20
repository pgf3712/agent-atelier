# Design story: teaching agents through a personal pixel studio

## A personal portfolio project

Paula & Indy's Agent Atelier was created to combine AI engineering, teaching and visual arts in one coherent project. The application is not decorated after the technical work; its visual language is part of the learning design.

The central metaphor is a creative studio built at night. An agent harness is assembled piece by piece in the same way that a workspace gains tools, notes, monitors and evidence over time. The environment becomes richer as the learner completes chapters.

## Paula and Indy

Paula is a stylised pixel-art guide inspired by the project's creator: long blonde hair, black glasses, hazel green-brown eyes and a dark hoodie. She represents explanation and technical depth. Clicking Paula opens a chapter-specific notebook with:

- the mental model;
- a concrete example;
- a common mistake;
- the real files connected by the chapter;
- a concise technical summary grounded in observable evidence.

Indy is inspired by Paula's Siamese cat. He represents optional support. His first interaction gives a contextual nudge; the exact answer remains behind a second deliberate action. This keeps help available without removing the learner's agency.

## Why pixel art?

Pixel art makes the course feel like a calm indie game while preserving a clear boundary between the educational product and a generic corporate dashboard. Large, deliberate pixels also allow each character pose to remain readable at small sizes.

The palette uses midnight navy and slate blue for the learning surface, warm lamps and gold for focus, mint for successful evidence, and pink only as a secondary personal accent.

## Visual progression

Each chapter introduces a different static pose and a new conceptual object in the studio. Movement is intentionally restrained:

- chapter portraits remain static to prevent flicker and distraction;
- the sleeping sidebar Indy breathes subtly;
- celebration animation appears only after completing the course;
- `prefers-reduced-motion` removes non-essential movement.

## Accessibility before decoration

Long text uses a readable sans-serif rather than a pixel font. Content sits on translucent navy panels with strong contrast. Keyboard focus is visible, status never depends on colour alone and private chain of thought is never presented as an educational feature.

## Asset disclosure

The production characters and background were created specifically for this project with AI-assisted image generation under Paula's direction, then processed for the interface. They do not contain copied Pinterest compositions, commercial game sprites or stock artwork. Full details are recorded in `ASSET_CREDITS.md`.
