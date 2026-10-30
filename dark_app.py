                            {title}
                        </div>
                        <div style="font-size:12px;line-height:1.65;
                                    color:{MUTED};margin-top:4px;">
                            {description}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div style="background:#10282B;border:1px solid #24584F;
                        border-radius:13px;padding:15px 17px;margin-top:15px;">
                <div style="font-size:10px;font-weight:900;letter-spacing:1.8px;
                            color:{MINT};">COMMANDER'S REMINDER</div>
                <div style="font-size:13px;line-height:1.75;color:#C4E2DB;margin-top:6px;">
                    A strong commander does not simply choose the biggest number.
                    They consider evidence, vulnerability, exposure, and the
                    limits of available resources.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with mission_right:
        st.markdown(
            f"""
            <div style="background:linear-gradient(145deg,#12243A,#0B1726);
                        border:1px solid #28758A;border-radius:19px;
                        padding:18px 18px 12px 18px;text-align:center;
                        box-shadow:0 12px 35px rgba(0,0,0,.22);">
                <div style="font-size:10px;letter-spacing:2.5px;
                            font-weight:900;color:{CYAN};">
                    SECURE MISSION ACCESS
                </div>
                <div style="font-size:23px;font-weight:900;color:{TEXT};
                            margin:8px 0 4px 0;">
                    ENTER ECO COMMANDER
                </div>
                <div style="font-size:12px;color:{MUTED};line-height:1.6;
                            margin-bottom:13px;">
                    Scan the mission portal with your phone camera.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        qr_path = Path(__file__).parent / "tera_lovable_qr.jpeg"
        if qr_path.exists():
            st.image(str(qr_path), use_container_width=True)
        else:
            st.warning(
                "QR image not found. Upload the supplied image to the same "
                "GitHub folder as app.py and name it tera_lovable_qr.jpeg."
            )

        st.markdown(
            f"""
            <div style="background:{PANEL};border:1px solid {BORDER};
                        border-radius:0 0 16px 16px;padding:13px;
                        text-align:center;margin-top:-8px;">
                <div style="font-size:11px;font-weight:900;letter-spacing:1.5px;
                            color:{MINT};">SCAN • LAUNCH • TAKE COMMAND</div>
                <div style="font-size:11px;color:{MUTED};margin-top:5px;">
                    TERA 2.0 // MIDNIGHT INTELLIGENCE EDITION
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.link_button(
            "🚀 LAUNCH ECO COMMANDER",
            "https://qrto.org/qdbhrj",
            use_container_width=True,
        )
        st.caption(
            "The launch button uses the same short link encoded in your supplied QR code."
        )

    st.markdown("")
    st.markdown(
        f"""
        <div style="border-top:1px solid {BORDER};padding:20px 8px 8px 8px;
                    text-align:center;">
            <div style="font-size:11px;font-weight:900;letter-spacing:2px;color:{CYAN};">
                THINK FAST. PRIORITISE WISELY. PROTECT THE FUTURE.
            </div>
            <div style="font-size:12px;color:{MUTED};margin-top:8px;">
                ECO COMMANDER is a companion educational game experience.
                Its scenarios and outcomes are simulated, not real emergency guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------------------- FOOTER --------------------
st.divider()
st.markdown(
    f"""
    <div style="text-align:center; padding:10px; color:{MUTED};">
        <div style="color:{CYAN}; font-weight:800; letter-spacing:2px;">
            TERA 2.0 • MIDNIGHT INTELLIGENCE
        </div>
        <div style="font-size:12px; margin-top:6px;">
            Technology for Environmental Risk Analysis
        </div>
        <div style="font-size:11px; margin-top:5px;">
            Educational prototype · Illustrative inputs · Not an operational early-warning system
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
