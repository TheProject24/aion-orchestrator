# - - - -Stage 1
FROM rust:slim as builder

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y protobuf-compiler

COPY proto ./proto

COPY gateway ./gateway

WORKDIR /usr/src/app/gateway
RUN cargo build --release

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /usr/src/app/gateway/target/release/gateway /usr/local/bin/gateway

CMD ["gateway"]